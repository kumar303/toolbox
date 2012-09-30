#!/usr/bin/python

"""compares work iTunes library with home iTunes library and 
reports any music that exists at work but not at home.
"""

import sys, os
import urllib
from collections import defaultdict

# Parse Apple's plist XML format, as used by iTunes for storing music
# information.
# Written by Fredrik Lundh as originally documented at
# http://online.effbot.org/2005_03_01_archive.htm
# That's not available anymore, though the Wayback Machine has it.

try:
    from xml.etree.cElementTree import iterparse
except ImportError:
    from xml.etree import iterparse
import base64, datetime, re, os
# from dateutil.parser import parse as parse_date

unmarshallers = {
    # collections
    "array": lambda x: [v.text for v in x],
    "dict": lambda x:
        dict((x[i].text, x[i+1].text) for i in range(0, len(x), 2)),
    "key": lambda x: x.text or "",

    # simple types
    "string": lambda x: x.text or "",
    "data": lambda x: base64.decodestring(x.text or ""),
    "date": lambda x:
        datetime.datetime(*map(int, re.findall("\d+", x.text))),
    "true": lambda x: True,
    "false": lambda x: False,
    "real": lambda x: float(x.text),
    "integer": lambda x: int(x.text),
}

def load(file):
    parser = iterparse(file)
    for action, elem in parser:
        unmarshal = unmarshallers.get(elem.tag)
        if unmarshal:
            data = unmarshal(elem)
            elem.clear()
            elem.text = data
        elif elem.tag != "plist":
            raise IOError("unknown plist type: %r" % elem.tag)
    return parser.root[0].text

# Search-and-replace strings to adjust the mp3's locations if necessary.
# sandrStrs = { "file://localhost/Volumes": "smb://sargent" }
sandrStrs = { "file://localhost": "" }

def main():

    try:
        work_lib_file, home_lib_file = sys.argv[1], sys.argv[2]
    except IndexError:
        print 'Usage: script.py "iTunes Music Library - Work.xml" "iTunes Music Library - Home.xml"'
        sys.exit()
    
    for lib_file in (work_lib_file, home_lib_file):
        if not os.path.isfile(lib_file):
            print "File %s doesn't exist." % lib_file
            sys.exit()
    
    work_library = load(work_lib_file)
    
    missing = open("find_missing_music.log",'w')
    num_existing = 0
    num_missing = 0
    # albums = defaultdict()
    
    home_library = load(home_lib_file)
    
    home_albums = set()
    for track in iter_tracks(home_library):
        home_albums.add(track.get('Album', 'Unknown Album'))
    
    missing_albums = set()
    album_artists = {}
    
    for track in iter_tracks(work_library):
        album_name = track.get('Album', 'Unknown Album')
        if album_name not in home_albums:
            missing_albums.add(album_name)
            album_artists.setdefault(album_name, [])
            album_artists[album_name].append(track.get('Artist', 'Unknown Artist'))
    
    for album_name in sorted(missing_albums):
        if len(album_artists[album_name]) == 1:
            artist_name = album_artists[album_name][0]
        else:
            artist_name = "V/A"
            
        missing.write("%s (%s)\n" % (album_name.encode('utf-8'), artist_name.encode('utf-8')))
    
    print ""
    print "Wrote %s" % missing.name
    missing.close()

def iter_tracks(library):
    # keys: ['Minor Version', 'Playlists', 'Features', 'Major Version', 
    # 'Library Persistent ID', 'Music Folder', 'Application Version', 'Tracks', 'Show Content Ratings']
    for k, track in library['Tracks'].iteritems():
        # The key in this case is the track ID number. The value is
        # a dict of all information associated with the track
        fileloc = track['Location']
        for old, new in sandrStrs.iteritems():
            fileloc = fileloc.replace(old, new)
        fileloc = urllib.unquote(fileloc)
        if 'iTunes/iTunes Music/' not in fileloc:
            # was never in the library anyway so we don't care
            continue
        
        yield track

if __name__ == '__main__':
    main()