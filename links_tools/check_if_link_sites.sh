if [ -f $1 ];
then
    cat $1 | tr 'A-Z' 'a-z' > /tmp/check_if_link_sites;
else
    echo $1 | tr 'A-Z' 'a-z' > /tmp/check_if_link_sites;
fi
for domain in `cat /tmp/check_if_link_sites`;
do
    links=`mysql -umingdatrade -ptrade@mingDA123 links -e "select * from site where site_domain like '%$domain%'" 2> /dev/null`;
    link_sites=`mysql -umingdatrade -ptrade@mingDA123 link_sites -e "select * from link_sites where site like '%$domain%'" 2> /dev/null`;
    #echo "mysql -umingdatrade -ptrade@mingDA123 links -e \"select * from site where site_domain like '%$domain%'\"";
    #echo "mysql -umingdatrade -ptrade@mingDA123 link_sites -e \"select * from link_sites where site like '%$domain%'\"";
    no_renew=`cat /tmp/no_renew_domains | grep $domain`;
    if [[ -z $no_renew ]];
    then
        if [[ ! -z $links ]];
        then
            echo "links: $domain";
        elif [[ ! -z $link_sites ]];
        then
            echo "link_sites: $domain";
        else
            echo "may be bussiness site: $domain";
        fi
    fi
    #result=`grep $domain ~/links/a.txt`
    #if [[ ! $result ]];
    #then
    #    echo $domain > /dev/null;
    #else
    #    echo $domain >> ~/links/b.txt;
    #fi
done
