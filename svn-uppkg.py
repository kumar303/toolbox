#!/usr/bin/env python

'''if you are tracking a package's releases in a versioned project, 
this will copy new files without disturbing '.svn' dirs 
'''
import optparse
import os
from os.path import join as pjoin
from shutil import copyfile

def main():
    parser = optparse.OptionParser(usage='%prog [options] pkg_dir version_dir' 
                                        + "\n\n" + __doc__.strip())
    parser.add_option('-n','--dry_run', action='store_true',
                                        help='print out what would happen')
    (options,args) = parser.parse_args()
    
    try:
        pkg_dir, version_dir = args
    except ValueError:
        parser.error('incorrect args')
        
    pkg_dir = os.path.realpath(pkg_dir)
    if pkg_dir[-1] != '/':
        pkg_dir = pkg_dir + '/'
    
    for root, dirs, files in os.walk(pkg_dir):
        for file in files:
            copy_from   = pjoin(root, file)
            copy_to     = pjoin(version_dir, root[len(pkg_dir):], file)
            to_parts    = copy_to.split('/')[:-1]
            to_root     = to_parts.pop(0)
            
            for part in copy_to.split('/')[:-1]:
                if part == '.':
                    continue
                dir = pjoin(to_root, part)
                if not os.path.isdir(dir):
                    if options.dry_run:
                        print "os.mkdir('%s')" % dir
                    else:
                        os.mkdir(dir)
                to_root = dir
                
            if options.dry_run:
                print "copyfile('%s', '%s')" % (copy_from, copy_to)
            else:
                copyfile(copy_from, copy_to)
        
        for d in dirs:
            if d.startswith('.'):
                dirs.remove(d)
        
    print 'Done'

if __name__ == '__main__':
    main()
