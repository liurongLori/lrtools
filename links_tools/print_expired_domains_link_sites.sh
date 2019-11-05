# coding=utf-8

NOW=$(date +%Y-%m-%d)
NO_RENEW_DOMAINS='/tmp/no_renew_domains'
mysql -umingdatrade -ptrade@mingDA123 link_sites -e "select site, date from link_sites where date < '$NOW'" 1> /tmp/link_sites_expire_domains 2> /dev/null
sed -i '/^site/d' /tmp/link_sites_expire_domains

expired_domains=''
while read site_info;
do
    site=`echo $site_info | cut -f1 -d' '`;
    date=`echo $site_info | cut -f2 -d' '`;
    domain=${site#*.};
    links=`mysql -umingdatrade -ptrade@mingDA123 links -e "select domain from domain where domain = '$domain'" 2> /dev/null`;
    if [[ -z $links ]] && [[ -z `grep $domain $NO_RENEW_DOMAINS` ]];
    then
        expired_domains+="$domain $date\n";
    fi
done </tmp/link_sites_expire_domains
echo -e $expired_domains

if [[ -z $expired_domains ]];
then
    TO='liurong@mbyte.tech';
    SUBJECT='以下old sites的域名即将过期，是否需要续费';
    BODY=$expired_domains;
    echo -e "To: $TO\nSubject: $SUBJECT\n$BODY" | /usr/sbin/ssmtp $TO -F "Backup REPORT" -f link;
fi
