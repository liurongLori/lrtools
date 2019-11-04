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
        upstreams_submit = {}
        for d in domains:
            domain = Domain.get(api.session(), d)
            assert domain is not None, 'The %s is invalid' % d
            if domain.upstream_sub_outbound:
                for upstream in domain.upstream_sub_outbound:
                    if upstream.site_domain in domains:
                        continue
                    upstreams_submit.setdefault(upstream.site_domain, [upstream.site.outbound_url])
                    if upstream.url not in upstreams_submit[upstream.site_domain]:
                        upstreams_submit[upstream.site_domain].append(upstream.url)
                    if upstream.site.homepage_type == 'independent' and upstream.site.outbound_type == 'sub_outbounds':
                        if upstream.site.domain.homepage_url() not in upstreams_submit[upstream.site_domain]:
                            upstreams_submit[upstream.site_domain].append(upstream.site.domain.homepage_url())
            else:
                for upstream in domain.get_upstream_domains():
                    if upstream.domain in domains:
                        continue
                    upstreams_submit.setdefault(upstream.domain, [upstream.site.outbound_url])

        for upstream_domain in upstreams_submit:
            upstream_desc = Domain.get(api.session(), upstream_domain)

            print('%s\t%s\t%s\t%s' % (upstream_desc.site.block_expire, upstream_desc.domain, upstream_desc.contact_email, upstreams_submit[upstream_domain]))
