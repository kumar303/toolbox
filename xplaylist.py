#!/usr/bin/env python

import os
import sys
from shutil import copyfile
import optparse
try:
    import cElementTree as ElementTree
except ImportError:
    from elementtree import ElementTree
from urllib import unquote
from os.path import join as pjoin

library = None
dry_run = False

def copy_song(copy_to, fn):

    fn_abs = unquote(fn.replace('file://localhost', ''))
    fn = fn.replace('file://localhost%s' % library, '')
    parts = fn.split('/')
    
    root = ''
    for p in parts[:-1]:
        root = pjoin(root, unquote(p))
        fdir = pjoin(copy_to, root)
        if not os.path.isdir(fdir):
            print 'mkdir "%s"' % fdir
            if not dry_run:
                os.mkdir( fdir, 0744)
        
    new_f = pjoin(copy_to, root, unquote(parts[-1]))
    print 'cp "%s" "%s"' % (fn_abs, new_f)
    if not dry_run:
        copyfile(fn_abs, new_f)

def extract_songs(playlist, copy_to):
    num_songs = 0
    
    pl = ElementTree.parse(playlist)
    dicts = pl.findall('dict')
    for d in dicts:
        for k in d.findall('key'):            
            if k.text == 'Tracks':
                for trk_d in d.findall('dict/dict'):
                    look_for_loc = False
                    
                    for child in trk_d.getchildren():
                        if child.tag == 'key' and child.text == 'Location':
                            look_for_loc = True
                        if child.tag == 'string' and look_for_loc:
                            copy_song(copy_to, child.text)
                            num_songs += 1
                            look_for_loc = False
                            break
    if dry_run:
        print "DRY RUN:",
    print "copied %d song(s) to %s" % (num_songs, copy_to)

def main():
    '''extract song files from an iTunes XML playlist'''
    global library, dry_run
    library = pjoin('/Users', os.environ['USER'], 'Music','iTunes')
    
    parser = optparse.OptionParser(usage='%prog playlist.xml' + "\n" + main.__doc__)
    parser.add_option('-c','--copy_to',
                        help='copy songs to this directory.  defaults to ./songs',
                        default=os.getcwd() + '/songs')
    parser.add_option('-l','--library', default=library,
                        help=   'iTunes music library directory.  '
                                'defaults to %s' % library)
    parser.add_option('-n','--dry_run', action='store_true', 
                        help="just prints what would happen")
    (options,args) = parser.parse_args()
    
    try:
        playlist, = args
    except ValueError:
        parser.error('incorrect arg count')
    
    library = options.library
    if library[-1] is not '/':
        library += '/'
    if options.dry_run:
        dry_run = True
    
    print "mkdir %s" % options.copy_to
    if not dry_run:
        os.mkdir( options.copy_to, 0744)
    
    extract_songs(playlist, options.copy_to)

if __name__ == '__main__':
    main()