if [ -f $1 ];
then
    cat $1 | tr 'A-Z' 'a-z' > /tmp/check_if_link_sites;
else
    echo $1 | tr 'A-Z' 'a-z' > /tmp/check_if_link_sites;
fi
for domain in `cat /tmp/check_if_link_sites`;
do
    links=`mysql -umingdatrade -ptrade@mingDA123 links -e "select * from domain where domain like '%$domain%'" 2> /dev/null`;
    extra_target_sites=`mysql -umingdatrade -ptrade@mingDA123 links -e "select * from extra_target_site where site_domain like '%$domain%'" 2> /dev/null`;
    link_sites=`mysql -umingdatrade -ptrade@mingDA123 link_sites -e "select * from link_sites where site like '%$domain%'" 2> /dev/null`;
    sites=`mysql -umingdatrade -ptrade@mingDA123 link_sites -e "select * from sites where site like '%$domain%'" 2> /dev/null`;
    #echo "mysql -umingdatrade -ptrade@mingDA123 links -e \"select * from domain where domain like '%$domain%'\"";
    #echo "mysql -umingdatrade -ptrade@mingDA123 link_sites -e \"select * from link_sites where site like '%$domain%'\"";
    #echo $domain;
    no_renew=`cat /tmp/no_renew_domains | grep $domain`;
    bussiness_site=`cat ~/lrtools/links_tools/bussiness_sites | grep $domain`;
    if [[ -z $no_renew ]];
    then
        if [[ ! -z $bussiness_site ]];
        then
            echo "bussiness site: $domain";
        elif [[ ! -z $links ]];
        then
            echo "links: $domain";
        elif [[ ! -z $extra_target_sites ]];
        then
            echo "extra_target_sites: $domain";
        elif [[ ! -z $link_sites ]];
        then
            echo "link_sites: $domain";
        elif [[ ! -z $sites ]];
        then
            echo "sites: $domain";
        else
            echo "useless site: $domain";
        fi
    else
        echo "no renew: $domain";
    fi
done
