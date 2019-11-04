from datetime import datetime
from api.data_model import Site
from api.arg_parser import ManagedArgumentParser

if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-d', '--domain', help="The domains you want to check the block_expire")
    parser.add_argument('-f', '--domains_file', help="The domains' file you want to check the block_expire")
    parser.add_argument('--modify', dest='modify', action='store_true')
    parser.add_argument('--no_modify', dest='modify', action='store_false')
    parser.set_defaults(dry_run=True, draw_graph=False, sanity_check=False, modify=False)
    args = parser.parse_args()

    with ManagedArgumentParser.api_by_args(args) as api:
        domains = []
        if args.domain:
            domains.append(args.domain)
        elif args.domains_file:
            with open(args.domains_file) as f:
                domains = f.readlines()
        assert len(domains) > 0, "Must input a domain or a domains' file"

        for domain in domains:
            domain_desc = api.session().query(Site).filter(Site.site_domain == domain.strip()).one_or_none()
            block_expire = domain_desc.block_expire
            now_time = datetime.now()
            if block_expire > now_time:
                new_block_expire = now_time.strftime('%Y-%m-%d %H:%M:%S')
                if args.modify:
                    domain_desc.block_expire = new_block_expire
                print('%s\t%s\tto\t%s' % (domain.strip(), block_expire, new_block_expire))
