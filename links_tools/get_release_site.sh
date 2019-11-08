#!/usr/bin/env bash

if [ "$1" != "again" ]
then
    cd ~/links/
    source venv/bin/activate
    python tests/dns_test.py --no_dry_run | cut -d ' ' -f 2 > /tmp/domains.txt
fi

for i in `cat /tmp/domains.txt`; do
    mysql -h52.52.129.244 -umingdatrade -ptrade@mingDA123 links -N -e "select block_expire, cdn, host_ip, site_domain, contact_email, entry_url, outbound_url, homepage_type, outbound_type from site, domain where domain.domain = site.site_domain and domain.domain = '$i'";
done > /tmp/d.txt

if [ "$2" != "no_sort" ]
then
    sort -t $'\t' -k 2 /tmp/d.txt > /tmp/dns.txt
else
    cp /tmp/d.txt /tmp/dns.txt
fi

cat /tmp/dns.txt
