#!/usr/bin/env python2.7

"""walks the current directory and looks for any repositories with uncommitted or unpushed changes.

Requires Python 2.7
"""

from contextlib import contextmanager
import os
import subprocess

def main():
    for filename in os.listdir(os.getcwd()):
        filename = os.path.join(os.getcwd(), filename)
        try:
            if os.path.isdir(filename):
                with chdir(filename):
                    if os.path.exists(os.path.join(filename, '.svn')):
                        output = call(['svn', 'status'])
                        if output:
                            print_where(filename)
                            print(output)
                    elif os.path.exists(os.path.join(filename, '.hg')):
                        output = call(['hg', 'status']) or call(['hg', 'outgoing'])
                        if output:
                            print_where(filename)
                            print(output)
        except:
            print_where(filename)
            raise

def print_where(filename):
    print("*"*20, filename, "*"*20)

@contextmanager
def chdir(newdir):
    olddir = os.getcwd()
    os.chdir(newdir)
    yield
    os.chdir(olddir)

def call(cmd):
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    main()