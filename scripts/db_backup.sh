#!/bin/bash
db_name="stu_system"
backup_dir="/root/workspace/db_backup/backup"
time=$(date +"%Y%m%d%H%M%S")
/usr/bin/mysqldump -uroot -p1q2w3e4r\!Q $db_name > "$backup_dir/$db_name"_"$time.sql"