#!/usr/bin/env python

"""takes an exchange event invitation email as stdin, finds the attached vcal file, and opens that as a meeting request file in ical """

import sys, os, re

v_begin = 'BEGIN:VCALENDAR'
v_end = 'END:VCALENDAR'
vcal_data = []
in_vcal = False
stdin_lines = sys.stdin.readlines()
stdin_str = "\n".join(stdin_lines)
SAVE_DIR = '/tmp'

for line in stdin_lines:
    line = str.rstrip(line)
    if line == v_begin:
        in_vcal = True
    if in_vcal:
        vcal_data.append(line)
    if line == v_end:
        in_vcal = False

meta = re.search(r'Content-Type: text/calendar;\s+name="(?P<filename>[^"]+)";\s+method=REQUEST', stdin_str)
filename = "%s/%s" % (SAVE_DIR, meta.group('filename'))

vcal = file(filename, 'w+')
vcal.write("\n".join(vcal_data))
vcal.close()

sys.exit(os.system('/usr/bin/open "%s"' % (filename)))