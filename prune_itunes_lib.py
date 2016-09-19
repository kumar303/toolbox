#!/usr/bin/env python

import os
import sys
from shutil import copyfile
import optparse
from xml.etree import ElementTree
from urllib import unquote
from os.path import join as pjoin
import pprint
from collections import defaultdict
from decimal import Decimal


def search_lib(library):
    library_xml = pjoin(library, 'iTunes Music Library.xml')
    pl = ElementTree.parse(library_xml)
    dicts = pl.findall('dict/dict/dict')
    skipped = 0
    found = 0

    print 'Looking for old unplayed albums'
    play_counts = defaultdict(list)
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
            title = u''
            if not track.get('Compilation'):
                title = u'{} - '.format(track['Artist'])
            title = u'{}{}'.format(title, track['Album'])
            play_counts[(track['Date Added'][0:10], title)].append(
                int(track['Play Count'] or 0))
            found += 1
        except KeyError:
            skipped += 1

    print 'Found: {}'.format(found)
    print 'Skipped: {}'.format(skipped)

    print 'Checking for rarely played albums'
    to_purge = []
    for key, counts in play_counts.iteritems():
        # Skip anything with less than 5 tracks because it's
        # not worth the time to delete these.
        if len(counts) < 5:
            continue
        # Purge anything that was only played once (on average)
        if (Decimal(sum(counts)) / Decimal(len(counts))) <= Decimal(1):
            to_purge.append(key)

    for year_added, release in sorted(to_purge):
        line = u'{} (Added on {})'.format(release, year_added)
        print line.encode('utf8')


def main():
    """Print a list of rarely played iTunes music, oldest first"""
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
