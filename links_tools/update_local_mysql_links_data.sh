#!/bin/bash
#
# 1. remote backup database link except tables like $ingore_tables and scp links_backup.sql to local
USER='mingdatrade'
PASS='trade@mingDA123'
DATABASE='links'
ingore_tables=(
    'links.p2_url'
    'links.target_site_url'
    'links.target_site_url_redirect'
    )
ingore_tables_string=""
for table in ${ingore_tables[@]};
do
    ingore_tables_string+=" --ignore-table=$table"
done
echo 'ssh link to mysqldumping database links ...'
ssh link -t "mysqldump -u$USER -p$PASS --databases $DATABASE $ingore_tables_string > /tmp/links_backup.sql"
echo 'ssh copying database links to local ...'
scp link:/tmp/links_backup.sql /tmp/

# 2. import the backup data to local mysql which data from remote mysql
echo 'importing database successfully ...'
mysql links < /tmp/links_backup.sql


# 3. insert the newest data about backup_tables from remote mysql by scripts
# 4. backup tables which from local database links can't backup successfully because of the connecting with other remote mysql
export LINKS_CONN_STR='mysql+pymysql://mingdatrade:trade@mingDA123@52.52.129.244/links'
backup_tables=(
    'target_site_url'
    'target_site_url_redirect'
    'p2_url'
    )
echo 'copying tables ...'
source ~/links/env/bin/activate
for backup_table in ${backup_tables[@]};
do
    python ~/tools/batch_insert_table_to_local_links.py --no_dry_run -t $backup_table;
    mysql links_backup -e "insert $backup_table select * from links.$backup_table";
done
