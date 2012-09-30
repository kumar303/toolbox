#!/bin/bash

# set files and locations:
DATE=`date +%Y-%m-%d`
DB_USERNAME=kumar
MYSQLDUMP_FILE=mysqldump-$DB_USERNAME-$DATE.sql
USERS_DIR=/Users

# set backup locations:
BACKUP_OWNER=kumar
BACKUP_DIR="/Volumes/incognito/backup"
BACKUP_DIR_MYSQL="$BACKUP_DIR/mysql"
BACKUP_DIR_USERS="$BACKUP_DIR/Users"

# find programs
BZIP2=`which bzip2`
BZIP2_EXT=.bz2
MYSQLDUMP=`which mysqldump`
TAR=`which tar`

function chown_backup
{
	echo "changing owner of $1 to $BACKUP_OWNER ... "
	chown $BACKUP_OWNER $1
	if [ $? -eq 0 ]; then
		 echo "$FUNCNAME $1 ok"
	else
		 echo "$FUNCNAME $1 Failed"
		 exit 12
	fi
}

function bzip_file
{
	echo "bzipping $1 ... "
	$BZIP2 $1
	if [ $? -eq 0 ]; then
		 echo "$FUNCNAME $1 ok"
	else
		 echo "$FUNCNAME $1 Failed"
		 exit 12
	fi
}

MYSQLDUMP_BACKUP_FILE=$BACKUP_DIR_MYSQL/$MYSQLDUMP_FILE
echo "dumping all databases to $BACKUP_DIR_MYSQL/$MYSQLDUMP_FILE ..."
$MYSQLDUMP --all-databases --add-drop-table -u $DB_USERNAME -p > $MYSQLDUMP_BACKUP_FILE
if [ $? -eq 0 ]; then
   echo "$MYSQLDUMP ok"
else
   echo "$MYSQLDUMP Failed"
   exit 12
fi
bzip_file $MYSQLDUMP_BACKUP_FILE
chown_backup $MYSQLDUMP_BACKUP_FILE$BZIP2_EXT

echo "looking for User dirs in $USERS_DIR ..."
for USER_DIR in `ls $USERS_DIR | grep -E "^[a-z0-9]+"`
do
	
	echo "backing up User dir $USERS_DIR/$USER_DIR ..."
	USER_DIR_BACKUP_FILE=$BACKUP_DIR_USERS/$USER_DIR-$DATE.tar
	$TAR -cf "$USER_DIR_BACKUP_FILE" "$USERS_DIR/$USER_DIR"
	if [ $? -eq 0 ]; then
		 echo "$TAR ok"
	else
		 echo "$TAR Failed"
		 exit 12
	fi
	bzip_file $USER_DIR_BACKUP_FILE
	chown_backup $USER_DIR_BACKUP_FILE$BZIP2_EXT

done

echo "backup completed successfully."
