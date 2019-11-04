import requests
from bs4 import BeautifulSoup
from furl import furl
import tldextract

from api.arg_parser import ManagedArgumentParser
from api.data_model import FamousThirdPartyResource, FamousOutlink


unexpected_str = ['google', 'cdn', 'api']
def crawl_source(famous_link_domains, url, type):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.ConnectionError:
        return

    crawl_links = []
    if type == 'image':
        for img in soup.find_all('img', src=True):
            crawl_links.append(img['src'])
    else:
        for script in soup.find_all('script', src=True):
            crawl_links.append(script['src'])

    self_domain = tldextract.extract(url).domain
    links = []
    for link in crawl_links:
        if not tldextract.extract(link).domain:
            continue
        if tldextract.extract(link).domain == self_domain:
            continue
        if tldextract.extract(link).domain in famous_link_domains:
            continue
        for s in unexpected_str:
            if s in link:
                break
        else:
            if furl(link).scheme and furl(link).host and furl(link).host.split('.')[-2] != self_domain:
                links.append(link)
    return set(links)


if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-fo', '--famous_outlink', help='The famous_outlink is used to crawl resources.')
    parser.add_argument('-fof', '--famous_outlinks_file', help="The famous_outlinks' file")
    parser.add_argument('-t', '--type', choices=['image', 'javascript'], required=True, help='The type of resources')
    parser.add_argument('-fru', '--famous_resource_url', help='The famous resource to be added')
    parser.add_argument('-fruf', '--famous_resource_urls_file', help="The famous resource urls' file to be added")
    parser.set_defaults(draw_graph=False)
    args = parser.parse_args()

    with ManagedArgumentParser.api_by_args(args) as api:
        if args.famous_outlink or args.famous_outlinks_file:
            urls = []
            if args.famous_outlink:
                urls.append(args.famous_outlink)
            else:
                with open(args.famous_outlinks_file) as f:
                    for url in f.readlines():
                        urls.append(url.strip())

            famoud_outlink = api.session().query(FamousOutlink).all()
            famous_link_domains = []
            for famous_link in famoud_outlink:
                famous_link_domains.append(tldextract.extract(famous_link.url).domain)
            famous_link_domains = set(famous_link_domains)
            n = 0
            with open('famous_urls', 'w') as f:
                for url in urls:
                    links = crawl_source(famous_link_domains, url, args.type)
                    if links:
                        for link in links:
                            f.write(link)
                            f.write('\n')
                            n += 1
            print('%d famous sources have been crawled' % n)
        elif args.famous_resource_url or args.famous_resource_urls_file:
            famous_resource_urls = []
            if args.famous_resource_url:
                famous_resource_urls.append(args.famous_resource_url)
            else:
                with open(args.famous_resource_urls_file) as fruf:
                    for fu in fruf:
                        famous_resource_urls.append(fu)

            m = 0
            for u in set(famous_resource_urls):
                if not u.strip():
                    continue
                q = FamousThirdPartyResource(url=u.strip(), type=args.type)
                api.session().merge(q)
                m += 1
            print('%d urls have been added' % m)
        else:
            args_stats = False
            assert  args_stats, 'Must require the action crawl url or add url, and use arg about famous_outlink or famous_resource_url'
