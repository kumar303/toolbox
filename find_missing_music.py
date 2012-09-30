#!/usr/bin/python

import sys, os
import urllib

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


def main():
    # Search-and-replace strings to adjust the mp3's locations if necessary.
    # sandrStrs = { "file://localhost/Volumes": "smb://sargent" }
    sandrStrs = { "file://localhost": "" }

    try:
        xmlFile = sys.argv[1]
        # date_of_last_backup_str = sys.argv[2]
    except IndexError:
        print 'Usage: script.py "iTunes Music Library.xml"'
        sys.exit()

    if not os.path.isfile(xmlFile):
        print "File %s doesn't exist."
        sys.exit()
    
    # date_of_last_backup = parse_date(date_of_last_backup_str)
    library = load(xmlFile)

    # keys: ['Minor Version', 'Playlists', 'Features', 'Major Version', 'Library Persistent ID', 'Music Folder', 'Application Version', 'Tracks', 'Show Content Ratings']
    missing = open("find_missing_music.log",'w')
    num_existing = 0
    num_missing = 0
    albums = set()
    for k, v in library['Tracks'].iteritems():
        # The key in this case is the track ID number. The value is
        # a dict of all information associated with the track
        fileloc = v['Location']
        for old, new in sandrStrs.iteritems():
            fileloc = fileloc.replace(old, new)
        fileloc = urllib.unquote(fileloc)
        if 'iTunes/iTunes Music/' not in fileloc:
            # was never in the library anyway so we don't care
            continue
            
        # if v['Date Modified'].date() >= date_of_last_backup:
        if not os.path.exists(fileloc):
            num_missing += 1
            track_key = make_key(v)
            if track_key not in albums:
                missing.write("%s %r\n" % (repr(track_key), fileloc))
                albums.add(track_key)
        else:
            num_existing += 1
        sys.stdout.write( "Existing: %s, Missing: %s\r" % (num_existing, num_missing))
    
    print ""
    print "Wrote %s" % missing.name
    missing.close()

def make_key(track):
    return (track['Artist'], track.get('Album', 'Unknown Album'))

if __name__ == '__main__':
    main()