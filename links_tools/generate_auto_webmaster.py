import argparse
import re

webmaster_site = '{"site": "webmaster", "auto_login": true}'
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--site_info_file', required=True,
            help='The info about site')
    args = parser.parse_args()

    with open(args.site_info_file) as f:
        for line in f.readlines():
            email = line.split("\t")[0]
            password = line.split("\t")[1]
            submit_urls = line.split("\t")[2:]
            except_urls = []
            for url in submit_urls:
                if "'" in url:
                    except_urls.append(url.replace("'", '*').strip())
                    submit_urls.remove(url)
            print('-u %s -p %s -c "%s" -f \'{"float panel": "%s"}\' -h \'%s%s\' -t \'%s\''% (
                    email, 'mBYTE123456', email,
                    ' '.join(except_url for except_url in except_urls),
                    ''.join('<button class="ac_bt_submit_url">%s</button>' % (u.strip()) for u in submit_urls),
                    '<button class="ac_bt_submit_all ac_bt_on_load_click ac_bt_on_finish_close">submit all</button>',
                    webmaster_site))

