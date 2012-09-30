#!/usr/bin/env python

import optparse
import os
import commands
import shutil

DEBUG = False

class CommandFail(Exception): pass

def do_cmd(cmd):
    if DEBUG:
        print 'DEBUG', cmd
    (status, outp) = commands.getstatusoutput(cmd)
    if status is not 0:
        raise CommandFail(outp)
    if outp:
        print outp

def mvsrc(srctree, built_dir):
    if not os.path.exists(built_dir):
        raise OSError("built_dir '%s' does not exist" % built_dir)
    
    srctree = os.path.abspath(srctree)
    src_archive = "%s.tar.bz2" % srctree
    cwd = os.path.abspath(os.getcwd())
    try:
        moveto = os.path.join(built_dir, os.path.basename(src_archive))
        print "Archiving %s to %s ..." % (srctree, moveto)
        
        os.chdir(os.path.dirname(srctree))
        do_cmd("tar -cjf %s %s" % (src_archive, os.path.basename(srctree)))
        os.rename(src_archive, moveto)
        shutil.rmtree(srctree)
        print "DONE"
    finally:
        os.chdir(cwd)
        if os.path.exists(src_archive):
            print "REMOVING %s" % src_archive
            os.unlink(src_archive) 

def main():
    """compresses a src tree, stores it in $built_dir, and removes it"""
    parser = optparse.OptionParser(usage='%prog dir' + "\n" + main.__doc__)
    
    d_built_dir = os.getenv('HOME') + '/built'
    parser.add_option('-b','--built_dir', metavar='DIR',
                        help="sends tar/bz archive to this dir (default: %s)" % d_built_dir,
                        default=d_built_dir)
    parser.add_option('-R','--recursive', action='store_true', default=False,
                        help="opens $dir and archives *all* directories within")
    parser.add_option('-v','--verbose', action='store_true', default=False,
                        help="turn on debug messages DEBUG")
    
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect arg count')
    
    if options.verbose:
        globals()['DEBUG'] = True
        
    root = args[0]
    if options.recursive:
        def listroot():
            for d in os.listdir(root):
                yield os.path.join(root, d)
        dirs = [d for d in listroot() if os.path.isdir(d)]
    else:
        dirs = [root]
    if len(dirs) == 0:
        parser.error("no directories to search")
        
    for d in dirs:
        mvsrc(d, options.built_dir)

if __name__ == '__main__':
    main()
