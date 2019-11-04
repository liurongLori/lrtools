for i in `cat $1`; do
    mysql -h52.52.129.244 -umingdatrade -ptrade@mingDA123 -Dlinks -e "insert into famous_third_party_resource (url, type) values ('$i', '$2');"
done
