#!/usr/bin/env bash

if [ $# -lt 1 ]; then
  echo "Usage: `basename $0` db_user [passwd]"
  exit 127
fi

USER=$1
# ask for passwd ...
MD_ARG="--all-databases --add-drop-table -u $USER -p"
if [ "${#2}" -gt 0 ]; then
    # or tack it on the end ...
    MD_ARG="${MD_ARG}${2}"
fi
DATE=`date +%Y-%m-%d`
FILENAME=mysqldump-$USER-$DATE.sql
R_SERVER=incognito.no-ip.org
R_USER=kumar
R_LOC='~/backup/www'

echo "dumping all databases to $FILENAME ..."
mysqldump $MD_ARG > $FILENAME
if [ $? -eq 0 ]; then
   echo "mysqldump ok"
else
   echo "mysqldump Failed"
   exit 12
fi

echo "bzipping $FILENAME ... "
bzip2 $FILENAME
if [ $? -eq 0 ]; then
   echo "bzip2 ok"
else
   echo "bzip2 Failed"
   exit 12
fi

FILENAME=$FILENAME.bz2

echo "copying dump to $R_SERVER ... "
scp $FILENAME $R_USER@$R_SERVER:$R_LOC/$FILENAME
if [ $? -eq 0 ]; then
   echo "scp ok"
else
   echo "scp Failed"
   exit 12
fi
echo "cleaning up ..."
rm $FILENAME
