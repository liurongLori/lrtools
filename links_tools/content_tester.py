from datetime import datetime, timedelta
import re
import time

from api.data_model import Domain, Site, FamousOutlink, TargetSiteURL, StaticData
import tldextract
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.orm.session import Session
from bs4 import BeautifulSoup

'''
Get all the instanced domains and their home/entry/outbound/sub_outbound
urls. For each of the url, request the url with a googlebot + googleip
and analyize the content:

1. Check the status code:
* 200 if should not block
* 503 if should block

2. check the links to see if they are as expected:
* entry: check if there is a link to the outbound
* outbound: check if
    - there is a link to the link_to_url if type == single
    - there are links to the sub_outbounds if type == sub_outbounds
    - there are links to the target if type == combined
* sub_outbound: check if
    - there is a link to the link_to_url

3. if optimize doukai, should check famous link and famous resource on
the outbound url.

4. There shall be no <!-- ????? --> in the content.
'''

from enum import Enum


class ClientType(Enum):
    OFFICE = 1
    GOOGLE_BOT = 2
    GOOGLE_HUMAN = 3


class PageType(Enum):
    ENTRY = 1
    OUTBOUND = 2
    HOME = 3
    SUB_OUTBOUND = 4
    STATIC = 5


class ClientConfig(object):
    def __init__(self, user_agent, pretend_google_ip, local_use_proxy=True):
        self.user_agent = user_agent
        self.pretend_google_ip = pretend_google_ip
        self.local_use_proxy = local_use_proxy

    def proxies(self):
        if self.pretend_google_ip:
            return {
                'http': 'http://avarsha:avarsha@52.21.99.193:31028',
                'https': 'https://avarsha:avarsha@52.21.99.193:31028'
            }
        if self.local_use_proxy:
            return {
                'http': 'http://avarsha:avarsha@52.42.247.144:31028',
                'https': 'https://avarsha:avarsha@52.42.247.144:31028'
            }
        else:
            return None

    def __repr__(self):
        if self.pretend_google_ip:
            return 'Google IP with UA: %s' % self.user_agent
        return 'Local IP with UA: %s' % self.user_agent


class ExpectedResults(object):
    def __init__(self):
        self.status_code = 200
        self.is_static_page = False
        self.famous_link = False
        self.may_have_famous_link = False
        self.famous_resouce = None
        self.links = []

    def check(self, session, response, url, client_config):
        assert response.status_code == self.status_code, \
            'Expected response code of %s: %d, but get %d for "%s"' % \
            (url, self.status_code, response.status_code, client_config)

        # Skip checking the content of a static page.
        if self.is_static_page:
            return

        html = response.text
        find_tags = re.findall(r'<!-- [A-Z]{2,4} -->', html)
        assert not find_tags, 'Should not contain placeholder tags: %s on url %s' % (''.join(find_tags), url)

        links_in_page = []
        if html:
            doc = BeautifulSoup(html, 'lxml')
            a_tag = doc.find_all('a', href=True)
            links_in_page = [a['href'] for a in a_tag if a['href']]

        # Compare self.links and links_in_page:
        extra_links = []

        for link in self.links:
            assert link in links_in_page, 'Link(%s) should appear on %s for %s' % (link, url, client_config)
        for link in links_in_page:
            if link not in self.links:
                extra_links.append(link)

        if self.famous_link:
            assert len(extra_links) >= 1, 'Should have at least 1 extra link as famous link on %s for %s.' % (url, client_config)
            for extra_link in extra_links:
                famous_link = FamousOutlink.get(session, extra_link)
                assert famous_link, 'Link %s not expected on page %s.' % (extra_link, url)
        elif self.may_have_famous_link:
            assert len(extra_links) <= 1, 'Should have at most 1 famous link on %s for %s: %s.' % (url, client_config, extra_links)
            if len(extra_links) == 1:
                famous_link = FamousOutlink.get(session, extra_links[0])
                assert famous_link, 'Link %s not expected on page %s.' % (extra_links[0], url)
        else:
            assert len(extra_links) == 0, 'Should not have extra links on %s for %s: %s.' % (url, client_config, extra_links)

        if self.famous_resouce:
            assert self.famous_resouce in response.text, 'Famous resource is not found on %s for %s' % (url, client_config)


    @staticmethod
    def get_expected_results(domain, client_type, page_type):
        assert domain.site
        expected = ExpectedResults()
        now = datetime.fromtimestamp(int(time.time()))
        if client_type != ClientType.OFFICE and (domain.site.block_expire >= now or domain.site.status == 'abandoned'):
            expected.status_code = 503
            return expected

        if client_type == ClientType.GOOGLE_HUMAN:
            expected.status_code = 503
            return expected

        # Should return normal response for all other cases. No need to
        # bother client_type any more.
        assert client_type in [ClientType.OFFICE, ClientType.GOOGLE_BOT]

        if page_type == PageType.HOME and domain.site.homepage_type == 'none':
            expected.status_code = 404
            session = Session.object_session(domain)
            if StaticData.get(session, domain.homepage_url()):
                expected.status_code = 200
                expected.is_static_page = True
            return expected

        if page_type == PageType.STATIC:
            expected.status_code = 200
            expected.is_static_page = True
            return expected

        expected.status_code = 200
        expected.famous_resouce = domain.site.famous_third_party_resource_url
        if domain.site.extra_outlink:
            if page_type == PageType.OUTBOUND or \
                (page_type == PageType.HOME and domain.site.homepage_type == 'outbound'):
                expected.famous_link = True

        def get_links_on_outbound(domain):
            assert domain.site
            if domain.site.outbound_type == 'single':
                if domain.site.is_downstream_instanced():
                    downstream = domain.site.downstream_domain
                    if not downstream or now - downstream.site.create_timestamp > timedelta(days=3):
                        return [domain.site.link_to_url]
                return []
            session = Session.object_session(domain)
            if domain.site.outbound_type == 'combined':
                target_urls = domain.site.get_urls_for_combined_outbound()
                return [u.url for u in target_urls]
            if domain.site.outbound_type == 'sub_outbounds':
                sub_outbound_urls = []
                for s in domain.site.sub_outbounds:
                    if s.status == 'invalid':
                        continue
                    if s.downstream_domain or s.downstream_p2_url or s.downstream_target_site_url:
                        sub_outbound_urls.append(s.url)
                return sub_outbound_urls

        def get_pending_index_sub_outbound_urls(domain):
            sub_outbound_urls = []
            for s in domain.site.occuppied_sub_outbounds:
                if not s.index_timestamp:
                    sub_outbound_urls.append(s.url)
            return sub_outbound_urls

        # Set the links:
        expected.links = []
        if page_type is PageType.OUTBOUND:
            expected.links = get_links_on_outbound(domain)
        elif page_type is PageType.ENTRY:
            if domain.entry_url == domain.site.outbound_url:
                expected.links = get_links_on_outbound(domain)
            else:
                if domain.site.entry_link_to == 'statics':
                    expected.links = [s.url for s in domain.site.static_data if s.content_type.startswith('text/html')]
                else:
                    assert domain.site.entry_link_to == 'outbound'
                    expected.links = [domain.site.outbound_url]
        elif page_type is PageType.HOME:
            assert domain.site.homepage_type != 'none', 'Should not happen.'
            if domain.site.homepage_type == 'outbound':
                expected.links = get_links_on_outbound(domain)
            elif domain.site.homepage_type == 'independent' and domain.site.outbound_type == 'sub_outbounds':
                expected.links = get_pending_index_sub_outbound_urls(domain)
            # links = [] if domain.site.homepage_type == 'independent' and domain.site.outbound_type != 'sub_outbounds'
        elif page_type is PageType.SUB_OUTBOUND:
            sub = domain.site.sub_outbounds[0]
            if sub.is_downstream_instanced():
                downstream = sub.downstream_domain
                if not downstream or now - downstream.site.create_timestamp > timedelta(days=3):
                    expected.links = [sub.link_to_url]
            if domain.is_functional():
                # Some sub_outbound on functional domain will have
                # one random famous out link on it to confuse an
                # inspector.
                expected.may_have_famous_link = True
        return expected



class TestCase(object):
    def __init__(self, url, client_config, expected_results):
        self.url = url
        self.client_config = client_config
        self.expected_results = expected_results

    def test(self, session):
        host = tldextract.extract(self.url).subdomain + '.' + tldextract.extract(self.url).domain + '.' + tldextract.extract(self.url).suffix
        try:
            response = requests.get(self.url,
                    headers={
                        'User-Agent': self.client_config.user_agent,
                        "X-host": host
                        },
                    proxies=self.client_config.proxies())
        except ConnectionError:
            return
        self.expected_results.check(session, response, self.url, self.client_config)

    @staticmethod
    def get_test_case(domain, client_type, page_type):

        def first_static_html(domain):
            for s in domain.site.static_data:
                if not s.content_type.startswith('text/html'):
                    continue
                if s.url in (domain.entry_url, domain.site.outbound_url):
                    continue
                if s.url == domain.homepage_url and domain.site.homepage_type != None:
                    continue
                return s.url
            return None

        url = {
            PageType.ENTRY: domain.entry_url,
            PageType.OUTBOUND: domain.site.outbound_url,
            PageType.HOME: domain.homepage_url(),
            PageType.SUB_OUTBOUND: domain.site.sub_outbounds[0].url if domain.site.sub_outbounds else None,
            PageType.STATIC: first_static_html(domain),
        }
        user_ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 ContentTester'
        google_bot_ua = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) ContentTester'
        client_config = {
            ClientType.OFFICE: ClientConfig(user_ua, False, False),
            ClientType.GOOGLE_BOT: ClientConfig(google_bot_ua, True, False),
            ClientType.GOOGLE_HUMAN: ClientConfig(user_ua, True, False),
        }
        testing_url = url[page_type]
        if not testing_url:
            return None
        return TestCase(testing_url, client_config[client_type],
                        ExpectedResults.get_expected_results(domain, client_type, page_type))


class ContentTester(object):
    def __init__(self, session):
        self.session = session

    def test_domain(self, domain, test_google=False):
        if domain.status != 'instanced':
            return
        if domain.cloud_provider():
            return

        assert domain.site, 'Instanced domain should always have site.'

        test_cases = []
        clients = [ClientType.OFFICE]
        if test_google:
            clients += [ClientType.GOOGLE_BOT, ClientType.GOOGLE_HUMAN]
        for client_type in clients:
            test_cases.append(
                TestCase.get_test_case(domain, client_type, PageType.OUTBOUND))
            if domain.entry_url != domain.site.outbound_url:
                test_cases.append(
                    TestCase.get_test_case(domain, client_type, PageType.ENTRY))
            if domain.homepage_url() not in [domain.entry_url, domain.site.outbound_url]:
                test_cases.append(
                    TestCase.get_test_case(domain, client_type, PageType.HOME))
            if domain.site.sub_outbounds:
                test_cases.append(
                    TestCase.get_test_case(domain, client_type, PageType.SUB_OUTBOUND))
            if domain.site.entry_link_to == 'statics':
                test_cases.append(
                    TestCase.get_test_case(domain, client_type, PageType.STATIC))

        for test in test_cases:
            if not test:
                continue
            test.test(self.session)

    def test_all_instanced_domains(self, test_google=False):
        domains = Domain.find(self.session, 'instanced')
        for domain in domains:
            try:
                self.test_domain(domain, test_google)
            except Exception as ex:
                print('Domain %s failure: %s' % (domain.domain, ex))
                continue
