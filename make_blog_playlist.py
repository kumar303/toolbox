#!/usr/bin/env python

import optparse
import sys
def main():
    p = optparse.OptionParser(usage=(
        "pbpaste | %prog\n\n"
        "Copy an iTunes playlist and pipe it through to get a compressed playlist."
    ))
    p.add_option('--encoding', 
        help='Text encoding, default works for iTunes: %default', 
        default='ISO-8859-2')
    (options, args) = p.parse_args()
    for i, line in enumerate(sys.stdin):
        if line.strip() == "":
            continue
        line = line.decode(options.encoding)
        parts = line.split("\t")
        if len(parts)==1:
            raise ValueError(
                "Expected tab-separated fields.  "
                "First line was: %r" % line)
        line = u"%s. %s -- %s" % (i+1, parts[3], parts[0])
        line = line.encode(options.encoding)
        print line
        
if __name__ == '__main__':
    main()