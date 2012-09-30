#!/usr/bin/env python

from lxml.html import parse
from urllib2 import urlopen, HTTPError
import os, sys, traceback

def main():
    tree = parse('http://funkandsoul.blogspot.com/')
    outdir = os.path.expanduser("~/Downloads/funkandsoul")
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for link in tree.xpath('//a'):
        href = link.get('href')
        if href and href.endswith('.mp3'):
            base = os.path.basename(href)
            toname = os.path.join(outdir, base)
            if os.path.exists(toname):
                print "already nabbed %s (%s)" % (href, toname)
                continue
            to = open(toname, 'wb')
            try:
                from_ = urlopen(href)
                buflen = 1024
                while 1:
                    buf = from_.read(buflen)
                    if not buf:
                        break
                    to.write(buf)
            except:
                etype, val, tb = sys.exc_info()
                print " ** error with: %s" % href
                if os.path.exists(to.name):
                    os.unlink(to.name)
                if issubclass(etype, HTTPError):
                    traceback.print_exception(etype, val, tb)
                    continue
                raise
            from_.close()
            to.close()
            print "nabbed %s" % href

if __name__ == '__main__':
    main()