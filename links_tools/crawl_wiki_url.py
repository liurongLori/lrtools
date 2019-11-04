import re
import requests
from googletrans import Translator
from pyquery import PyQuery as pq
from api.arg_parser import ManagedArgumentParser
from api.data_model import Text
from tools.utils import ParsedDoc
from api.utils import md5
import re

headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def carwl_base_page(url):
    response = requests.get(url, headers=headers)
    doc = ParsedDoc(response.text, url, inline_css=False, parser_name='html.parser')
    items = doc.extract_href()
    urls = []
    for item in items:
        if 'en.wikipedia.org' not in item:
            continue
        if item in urls:
            continue
        urls.append(item)
        yield item


if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-u', '--url', help='Start url.')
    parser.add_argument('-f', '--urls_file', help="The urls' file")
    parser.add_argument('-la', '--language', choices=['en', 'fr', 'de'],
                        default='en', help='Select language for text[en|fr|de]')
    args = parser.parse_args()

    if args.urls_file:
        with open(args.urls_file) as f:
            urls = f.readlines()
    else:
        urls = [args.url]
    with ManagedArgumentParser.api_by_args(args) as api:
        n = 0
        for base_url in urls:
            assert base_url is not None, 'Must input url or the file for urls'
            for url in carwl_base_page(base_url.strip()):
                #for wikipedia_content in get_wikipedia_content(url):
                #    wikipedia_content = re.sub(r'\[[0-9]+\]', '', wikipedia_content)
                #    if args.language != 'en':
                #        wikipedia_content = Translator().translate(wikipedia_content, dest=args.language).text

                #    doc = ParsedDoc(wikipedia_content, base_url=md5(wikipedia_content), inline_css=False, parser_name='html.parser')
                #    doc.insert_comment(' TAG ')
                #    Text.add(api.session(), doc.dump(), 'wiki_content', language=args.language, merge=True)
                #    n += 1
                print(url)
                n += 1
        print('urls number: %d' % n)
        #print('add content num: %d' % n)

