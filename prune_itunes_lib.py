#!/usr/bin/env python

import os
import sys
from shutil import copyfile
import optparse
from xml.etree import ElementTree
from urllib import unquote
from os.path import join as pjoin
import pprint

def search_lib(library):
    library_xml = pjoin(library, 'iTunes Music Library.xml')
    pl = ElementTree.parse(library_xml)
    dicts = pl.findall('dict/dict/dict')
    to_purge = set()
    skipped = 0
    found = 0

    print 'Looking for old unplayed albums'
    for d in dicts:
        track = {}
        key = 'Unknown'
        for child in d.getchildren():
            if child.tag == 'key':
                key = child.text
            else:
                value = child.text
                if child.tag == 'true':
                    value = True
                track[key] = value

        #pprint.pprint(track)

        try:
            if int(track['Play Count']) <= 1:
                title = u''
                if not track.get('Compilation'):
                    title = u'{} - '.format(track['Artist'])
                title = u'{}{}'.format(title, track['Album'])
                to_purge.add((track['Date Added'][0:10], title))
                found += 1
        except KeyError:
            skipped += 1

    print 'Found: {}'.format(found)
    print 'Skipped: {}'.format(skipped)

    for year_added, release in sorted(to_purge):
        line = u'{} ({})'.format(release, year_added)
        print line.encode('utf8')

def main():
    '''extract song files from an iTunes XML playlist'''
    default_library = pjoin('/Users', os.environ['USER'], 'Music', 'iTunes')

    parser = optparse.OptionParser(usage='%prog' + "\n" + main.__doc__)
    parser.add_option('-l','--library', default=default_library,
                        help=   'iTunes music library directory.  '
                                'defaults to %s' % default_library)
    (options,args) = parser.parse_args()

    library = options.library
    if library[-1] is not '/':
        library += '/'

    search_lib(library)

if __name__ == '__main__':
    main()
