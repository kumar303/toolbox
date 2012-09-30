#!/usr/bin/env python

"""cleans the shell then executes command

... same thing as typing:
$ clear; command [arg [arg]]
designed for repeatedly running unit tests"""

import os, sys

def main():
	if len(sys.argv) < 2:
		print "error: no command to execute"
		return 1
	
	if sys.argv[1] in ('-h', '--help'):
		print __doc__
		return 0
	if sys.argv[1] in ('-t', '--test'):
		test()
		return 0
		
	command = ' '.join(sys.argv[1:])
	os.system('clear')
	return os.system(command)
	
def test():
	binpath = os.path.realpath(__file__)
	bintest = '%s ls -l ~' % binpath
	print "executing: '%s'" % bintest
	os.system(bintest)

if __name__ == '__main__':
	sys.exit(main())