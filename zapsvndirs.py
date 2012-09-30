#!/usr/bin/env python

import optparse
import os
import sys
from shutil import rmtree
from pydoc import getdoc
    
def main(): 
    """
    removes hidden svn directories
    """
    p = optparse.OptionParser(usage=("%prog [options] startdir" + 
                                        "\n\n" + getdoc(main)))
    p.add_option('-r','--remove', metavar='NAME',
            help="name of hidden dir to remove (default: .svn)", 
            default=".svn")
    (options, args) = p.parse_args()
    
    try:
        startdir = args[0]
    except IndexError:
        p.error("incorrect args")
        
    if not os.path.isdir(startdir):
        p.error("%s is not a directory" % startdir)

    for root, dirs, files in os.walk(startdir):
        print "walking:", root
        if options.remove in dirs:
            dirs.remove(options.remove)
            gettingzapped = os.path.join(root, options.remove)
            print "REMOVING:", gettingzapped
            rmtree(gettingzapped)
        
    print "done."
    
if __name__ == '__main__':
    main()