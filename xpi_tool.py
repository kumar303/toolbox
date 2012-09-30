#!/usr/bin/env python
import glob
import optparse
import os
import subprocess

def main():
    p = optparse.OptionParser(usage='%prog directory [options]')
    (options, args) = p.parse_args()
    if len(args) != 1:
         p.error('incorrect args')
    dirname = args[0]
    if dirname[-1] == '/':
        dirname = dirname[:-1]
    dest = "%s.xpi" % os.path.abspath(dirname)
    if os.path.exists(dest):
        print "Removing %r" % dest
        os.unlink(dest)
    os.chdir(dirname)
    zip = ['zip', '-9v', dest]
    zip.extend(list(os.listdir(os.getcwd())))
    print zip
    subprocess.check_call(zip)

if __name__ == '__main__':
    main()
