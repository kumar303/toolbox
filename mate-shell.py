#!/usr/bin/env python

import sys
import subprocess
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from traceback import format_exception

def main():
    # read stdin and pipe last statement through python, return a session with new results.
    # this really needs to be buffered, pickling could do that.
    chunks = [['']]
    chkid = 0
    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        if len(line) < 4:
            line = '... '
        if line.startswith('>>> '):
            chunks.append([''])
            chkid = chkid + 1
        chunks[chkid].append(line[4:])
    
    env = {}
    sysout = sys.stdout
    for code in chunks:
        output = ''
        buf = StringIO()
        try:
            sys.stdout = buf
            try:
                eval("\n".join(code), env)
            except:
                output = "".join(format_exception(*sys.exc_info()))
            else:
                output = buf.getvalue().strip()
        finally:
            sys.stdout = sysout
        
        # print len(code)
        print ">>> %s" % code[0]
        for line in code[1:]:
            print "... %s" % line
        if output:
            print output

if __name__ == '__main__':
    main()