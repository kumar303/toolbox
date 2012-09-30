#!/bin/sh
# Usage: `git examine <url>`
#
# * opens the github page if it found the file
#
# Only for the Mac.

if [[ $1 ]]; then
FILE=$1
else
FILE=''
fi

ROOT=$(git config remote.origin.url | perl -pi -e 's%^.*:(.*).git%https://github.com/\1/blob/master%')

echo $ROOT/$FILE '\c' | pbcopy
echo $FILE

# Open the browser.
open $ROOT/$FILE
