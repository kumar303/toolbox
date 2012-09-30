#!/usr/bin/env python

import os
import optparse
import sre
from os.path import join
from subprocess import Popen, PIPE
import inspect
import sys

def logall(start, xtra_args=None, verbose=False, dry_run=False):
    paths = []    
    
    svn = Popen(['svn', 'info', start], stdout=PIPE)
    url_p = sre.compile(r'^URL: (.*)')
    url = None
    for line in svn.stdout:
        m = url_p.match(line)
        if m:
            url = m.group(1)
    assert url is not None, "svn info: could not find URL:"
    
    paths = []
    svn = Popen(['svn', 'list', '--recursive', url], stdout=PIPE)
    [paths.append(L.strip()) for L in svn.stdout]
    r = svn.wait()
    if r != 0:
        print "\n".join(paths)
        sys.exit(r)
    
    cmd = ['svn']
    if xtra_args:
        cmd.extend(xtra_args)
    cmd.extend( ['log', url] )
    cmd.extend(paths)
    
    # if verbose or dry_run:
    #     print ' '.join(cmd)
    if dry_run:
        sys.exit(0)
        
    svn = Popen(cmd, stdout=PIPE)
    for line in svn.stdout:
        print line,

def main(argv=sys.argv[1:]):
    """recursively prints ALL unique revisions in a checkout directory by 
    looking up the URL with svn info then passing all its relative paths to svn 
    log.  this works around bugs in subversion server 1.2.3
    
    all options are echoed to the `svn log` command
    """
    argv_set = set(argv)
    if '-h' in argv_set or '--help' in argv_set:
        print "usage: %s [directory] [svn log options]\n\n%s" % (
                os.path.basename(sys.argv[0]), inspect.getdoc(main))
        sys.exit(0)
    if len(argv) and not argv[0].startswith('-'):
        start_dir = argv[0]
        argv = argv[1:]
    else:
        start_dir = os.getcwd()
    
    verbose = ('-v' in argv_set or '--verbose' in argv_set)
    logall(start_dir, xtra_args=argv, verbose=verbose )

if __name__ == '__main__':
    main()