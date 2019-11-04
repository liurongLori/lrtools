from api.data_model import Domain, Site
from api.utils import fetch_custom_page
from api.arg_parser import ManagedArgumentParser

if __name__ == '__main__':
    #        url = 'http://www.aboutbay.com/custom_page'
    #        custom_url = 'http://www.aboutbay.com/hello-the-war/'
    #        text_md5 = "8c042a69b6b14fadd2dd76dcbbac8e02"
    #        insert_extra_links = 1
    #        famous_third_party_resource_url = None
    #        links = [
    #                "http://www.wellingtonna.com/lots-of-crunching-and/",
    #                "http://www.wellingtonna.com/i-ve-heard-it/"
    #                ]
    #        fetch_custom_page(url, custom_url, text_md5, links, insert_extra_links, famous_third_party_resource_url)
    parser = ManagedArgumentParser()
    parser.set_defaults(confirm=False, draw_graph=False, test_google=False, sanity_check=False, dry_run=False)
    args = parser.parse_args()
    with ManagedArgumentParser.api_by_args(args) as api:
        links_to = ['http://www.wellingtonna.com/lots-of-crunching-and/']
        bucket_name = 'halo'
        site = Site.get(api.session(), 'aboutbay.com')
        content = site.serialize_to_static_data(links_to, bucket_name)
        print(content)

