import traceback
from datetime import datetime, timedelta
from api.data_model import Domain, ExtarTargetSite
from api.arg_parser import ManagedArgumentParser


if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-sd', '--source_domains', default='/tmp/no_renew_domains')
    parser.set_defaults(draw_graph=False)
    args = parser.parse_args()

    with ManagedArgumentParser.api_by_args(args) as api:
        with open(args.source_domains) as f:
            source_domains = [d.strip() for d in f.readlines()]
        for d in source_domains:
            domain = Domain.get(api.session(), d)
            if not domain:
                extra_target_site = ExtarTargetSite.get(api.session(), d)
                print('Extra target site %s has been expired, need to delete from table.' % d)
                if not extra_target_site:
                    continue
            expire_time = domain.registered_timestamp + timedelta(days=365)
            now_time = datetime.now()
            expire_days = expire_time - now_time
            if expire_days.days <= 0:
                if domain.status != 'abandoned':
                    print('%s expired at %s, update %s -> %s' %
                        (d, domain.registered_timestamp, domain.status, 'abandoned'))
                    domain.status = 'abandoned'
                    if domain.site:
                        domain.site.status = 'abandoned'

