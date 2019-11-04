import argparse

google_account_site = '{"site": "google_account", "auto_login": true}'
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--google_info_file', required=True,
            help='The info about google account')
    args = parser.parse_args()

    with open('/home/liurong/auto_chrome/google_account.in', 'w') as in_f:
        with open(args.google_info_file) as f:
            for line in f.readlines():
                email, password, assistant_email = line.split()
                #print('-u %s -p %s -c \'%s\' -f \'{"float panel": "%s %s"}\' -t %s % (email, password, assistant_email, 'mBYTE123456', assistant_email, google_account_site))
                in_f.write('-u %s -p %s -c \'%s\' -f \'{"float panel": "%s %s %s"}\' -t \'%s\'\n' % 
                        (email, password, assistant_email, password, 'mBYTE123456', assistant_email, google_account_site))
