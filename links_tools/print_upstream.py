from api.data_model import Domain, Site
from api.arg_parser import ManagedArgumentParser

if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-f', '--file_name',
                        help="The domains in file will be found the upstream sites info")
    parser.add_argument('-d', '--domain',
                        help="There will be found the upstream site info for this domain")
    parser.set_defaults(dry_run=False, confirm=False, draw_graph=False,
                        sanity_check=False)
    args = parser.parse_args()

    assert args.file_name or args.domain, 'Must input a arg'
    if args.file_name:
        with open(args.file_name) as f:
            domains = [domain.strip() for domain in f.readlines()]
    elif args.domain:
        domains = [args.domain]

    with ManagedArgumentParser.api_by_args(args) as api:
        upstreams = {}
        for d in domains:
            domain = Domain.get(api.session(), d)
            assert domain is not None, '%s is invalid' % d
            upstreams.setdefault(domain.domain, [])
            if domain.get_upstream_domains():
                for upstream in domain.get_upstream_domains():
                    upstreams[domain.domain].append(upstream.domain)

        for d in upstreams.items():
            print(d)
