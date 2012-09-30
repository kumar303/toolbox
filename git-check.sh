# Runs new and changed Python files through check.py and other checks
# https://github.com/jbalogh/check
if [ "$1" = "--help" ]; then
    echo "usage: `basename $0` [<commit>{0,2}]"
    exit 1
fi
if [ "$1" != "" ]; then
    REV=$1
fi
git diff $REV --check
git diff --cached --check
git diff $REV --name-status | grep .py | awk '$1 != "R" { print $2 }' | xargs check.py
git diff --cached --name-status | grep .py | awk '$1 != "D" { print $2 }' | xargs check.py
