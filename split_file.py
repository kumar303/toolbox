#!/usr/bin/env python

"""Splits a file into a new file without disturbing the original
file's descriptor.  This is useful for archiving a log when a
web server is constantly writing to it.
"""

import os
import optparse
import re

def main():
    p = optparse.OptionParser(usage="%prog [options] file.log\n\n" + __doc__)
    (options, args) = p.parse_args()
    if len(args) != 1:
        p.error("Incorrect usage")
    fname = args[0]
    new_fname = increment_n(fname)
    new_f = open(new_fname,'wb')
    old_f = open(fname, 'r+b')
    buf = 1024
    chunk = old_f.read(buf)
    while chunk:
        new_f.write(chunk)
        chunk = old_f.read(buf)
    old_f.seek(0)
    old_f.truncate()
    old_f.close()
    new_f.close()
    print "%r -> %r" % (old_f.name, new_f.name)

def increment_n(name, num=1):
    base = name
    m = re.search(r'\.(\d+)$', name)
    if m:
        base = base[ :base.rfind('.') ]
        num = int(m.group(1)) + 1
    new_fname = "%s.%d" % (base, num)
    if os.path.exists(new_fname):
        return increment_n(new_fname, num=num+1)
    else:
        return new_fname

# copy/paste into a shell!
# (lame)
test_script = """
pushd ~/tmp
rm -fr split_file_test
mkdir split_file_test
pushd split_file_test
echo "foo" > foo.txt
echo "bar" > foo.txt.2
split_file.py foo.txt
split_file.py foo.txt.1
cat foo.txt
cat foo.txt.3
popd
ls -1 split_file_test/
popd

"""
# should be
#   foo.txt
#   foo.txt.1
#   foo.txt.2
#   foo.txt.3
#


if __name__ == '__main__':
    main()
