#!/usr/bin/env python

import re, os, optparse, subprocess, inspect

def main():
    """"%prog [options] [checkout]"
    
    apply a command to all modified files in your svn status
    """
    p = optparse.OptionParser(usage=inspect.getdoc(main))
    p.add_option('--command', help=(
        "command to apply to a filename (filename arg appends to the end)"))
    (options, args) = p.parse_args()
    try:
        checkout = args[0]
    except IndexError:
        checkout = os.getcwd()
    stat = subprocess.Popen(['svn', 'stat', checkout], stdout=subprocess.PIPE)
    wtspace = re.compile("\s+")
    if not options.command:
        options.command = raw_input(
            "command to run each modified file through? ")
    compiled_cmds = []
    while 1:
        line = stat.stdout.readline()
        if not line:
            break
        status, filename, trail = wtspace.split(line)
        
        if status == '?':
            continue
        c = options.command + " " + filename
        compiled_cmds.append(c)
        print "  %s" % c
    x = stat.wait() 
    if x != 0:
        raise OSError("svn stat exited: %s" % x)
    
    applied = 0
    if raw_input("execute all commands? [Y/n] ") == 'Y':
        for cmd in compiled_cmds:
            os.system(cmd)
            applied += 1
    else:
        print "**nothing executed**"
            
    print "applied to %s file%s" % (
            applied==1 and (applied, "") or (applied, "s"))
    
if __name__ == '__main__':
    main()