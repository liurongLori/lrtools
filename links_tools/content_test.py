from tests.content_tester import ContentTester
from api.arg_parser import ManagedArgumentParser
from api.data_model import Domain


if __name__ == '__main__':
    parser = ManagedArgumentParser()
    parser.add_argument('-d', '--domain', default=None,
        help='The domain to upload contents for. Otherwise all domains.')
    parser.add_argument('--test_google', dest='test_google', action='store_true',
        help='Should have already set the DNS so that proxy ip can resolve the domains successfully.')
    parser.add_argument('--no_test_google', dest='test_google', action='store_false')
    parser.add_argument('-f', '--domain_file')
    parser.set_defaults(confirm=False, draw_graph=False, test_google=False)

    args = parser.parse_args()
    with ManagedArgumentParser.api_by_args(args) as api:
        t = ContentTester(api.session())
        if args.domain:
            domain = Domain.get(api.session(), args.domain)
            assert domain, args.domain
            t.test_domain(domain, args.test_google)
        if args.domain_file:
            with open(args.domain_file) as f:
                for d in f.readlines():
                    domain = Domain.get(api.session(), d.strip())
                    assert domain, d.strip()
                    t.test_domain(domain, args.test_google)
        else:
            t.test_all_instanced_domains(args.test_google)
