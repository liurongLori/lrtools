#!/bin/bash
export PYTHONPATH=":/home/liurong/links/"
export LINKS_CONN_STR="mysql+pymysql://mingdatrade:trade@mingDA123@52.52.129.244/links"
cd ~/links/
source env/bin/activate
#python tests/content_test.py --no_dry_run &>  /tmp/content_test_`date +%F`.log &&\
#    python tests/sanity_check.py --no_dry_run --no_draw_graph &>  /tmp/sanity_check_`date +%F`.log
#    python tools/draw.py --no_draw_hosts --no_dry_run &&\
#    python tools/print_resources.py --no_dry_run &> /tmp/print_resources_`date +%F`.log &&\
#    python tests/dns_test.py --no_dry_run &>  /tmp/dns_test_`date +%F`.log &&\


