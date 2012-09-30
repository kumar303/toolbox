#!/bin/bash

function usage()
{
    echo ""
    echo "usage: $0 /path/to/file.ext revision_num"
    echo "the old version will be saved as [filename].[revision_num].ext"
    echo ""
}

if [ $# -ne 2 ]
then
    usage
    exit 0
fi

FILEPATH=$1
ext=${FILEPATH##*.}
REVISION_NUM=$2
OUTPUT_FILE=${FILEPATH%.*}.$REVISION_NUM.$ext

cvs up -p -r $REVISION_NUM $FILEPATH > $OUTPUT_FILE
if [ $? -ne 0 ]
then
    echo "cvs failed"
    exit 1
fi

echo "saved $FILEPATH, revision $REVISION_NUM, to $OUTPUT_FILE"