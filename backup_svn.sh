#!/usr/bin/env bash

ARCHIVE=repo-`date +%Y-%m-%d`.tar.bz2
TMP_ARCHIVE=~/tmp/$ARCHIVE

cd ~/svn
echo "archiving svn repo ..."
tar -cjf $TMP_ARCHIVE repo
echo "backing up ..."
scp $TMP_ARCHIVE kumar@incognito.no-ip.org:~/backup/svn/$ARCHIVE
if [ -f $TMP_ARCHIVE ]; then
    echo "cleaning up ..."
    rm $TMP_ARCHIVE
fi
echo "done"