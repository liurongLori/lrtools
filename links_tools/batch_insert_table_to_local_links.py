import os

from api.arg_parser import ManagedArgumentParser
from api.data_model import TargetSiteURL, TargetSiteURLRedirect, P2URL

table_names = {
        'target_site_url': TargetSiteURL,
        'target_site_url_redirect': TargetSiteURLRedirect,
        'p2_url': P2URL,
        }

if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-n', '--number')
    parser.add_argument('-t', '--table', choices=table_names.keys(), required=True)
    parser.set_defaults(dry_run=True, confirm=False, draw_graph=False, sanity_check=False)

    args = parser.parse_args()
    table_name = table_names[args.table]

    with ManagedArgumentParser.api_by_args(args) as api:
        if args.number:
            target_site = api.session().query(table_name).limit(args.number)
        else:
            target_site = api.session().query(table_name).all()

        with open('insert_url', 'w') as f:
            for target in target_site:
                insert_cmd = 'insert into %s (%s) values ("%s");' % (args.table, \
                        ', '.join(column.key for column in table_name.__table__.columns), \
                        '", "'.join(str(target.__dict__[column.key]) for column in table_name.__table__.columns)
                        )
                select_cmd = 'select %s from %s where %s = "%s"' % (str(table_name.__mapper__.primary_key[0].key), \
                        args.table, str(table_name.__mapper__.primary_key[0].key), \
                        target.__dict__[str(table_name.__mapper__.primary_key[0].key)],
                        )

                os.system('mysql -uroot -plori links -e \'%s\' > log' % select_cmd)
                #print('mysql -uroot -plori links -e \'%s\' > log' % select_cmd)
                with open('./log')  as log:
                    if len(log.readlines()) == 0:
                        f.write(target.url)
                        f.write('\n')
                        os.system('mysql -uroot -plori links -e \'%s\'' % insert_cmd)
                        #print('mysql -uroot -plori links -e \'%s\'' % insert_cmd)

