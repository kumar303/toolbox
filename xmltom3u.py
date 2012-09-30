#!/usr/bin/python

# Convert an iTunes-exported XML playlist to m3u format
#
# Author: Stephen Granade
# Date: 2 January 2009

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
m3uHeader = "#EXTM3U\n"

try:
       xmlFile = sys.argv[1]
except IndexError:
       print "No xml file passed on the command line."
       sys.exit()

if not os.path.isfile(xmlFile):
       print "File %s doesn't exist."
       sys.exit()

playlist = load(xmlFile)

# Base the output filename on the input one, stripping off any '.xml'
# or similar from the right and adding in .m3u
outfn = xmlFile.rsplit('.',1)[0]+'.m3u'

outf = open(outfn, 'w')

# Write the M3U header
outf.write(m3uHeader)

# Iterate through the tracks to get each one's location and name
for k, v in playlist['Tracks'].iteritems():
       # The key in this case is the track ID number. The value is
       # a dict of all information associated with the track
       fileloc = v['Location']
       for old, new in sandrStrs.iteritems():
              fileloc = fileloc.replace(old, new)
       fileloc = urllib.unquote(fileloc)
       outf.write(fileloc+"\n")

outf.close()
