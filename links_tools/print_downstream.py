from api.data_model import Domain, Site
from api.arg_parser import ManagedArgumentParser

if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-f', '--file_name',
                        help="The domains in file will be found the downstream sites info")
    parser.add_argument('-d', '--domain',
                        help="There will be found the downstream site info for this domain")
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
        downstreams_submit = {}
        for d in domains:
            domain = Domain.get(api.session(), d)
            assert domain is not None, 'The %s is invalid' % d
            if domain.get_downstream_domains():
                for downstream in domain.get_downstream_domains():
                    if downstream.site_domain in domains:
                        continue
                    downstreams_submit.setdefault(downstream.site_domain, [downstream.site.outbound_url])
                    if downstream.url not in downstreams_submit[downstream.site_domain]:
                        downstreams_submit[downstream.site_domain].append(downstream.url)
                    if downstream.site.homepage_type == 'independent' and downstream.site.outbound_type == 'sub_outbounds':
                        if downstream.site.domain.homepage_url() not in downstreams_submit[downstream.site_domain]:
                            downstreams_submit[downstream.site_domain].append(downstream.site.domain.homepage_url())
            else:
                for downstream in domain.get_downstream_domains():
                    if downstream.domain in domains:
                        continue
                    downstreams_submit.setdefault(downstream.domain, [downstream.site.outbound_url])

        for downstream_domain in downstreams_submit:
            downstream_desc = Domain.get(api.session(), downstream_domain)

            print('%s\t%s\t%s\t%s' % (downstream_desc.site.block_expire, downstream_desc.domain, downstream_desc.contact_email, downstreams_submit[downstream_domain]))
