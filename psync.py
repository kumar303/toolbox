#!/usr/bin/env python

"""Sync projects from a local sandbox to a remote sandbox via rsync

In most cases the script will figure out the options for you.  See usage for details.
Some examples:

psync.py [kumar@]dev2/local_dir
psync.py -d big_directory
psync.py -f filename.txt
psync.py -u another_username -H another_server
psync.py -p my_project.tmproj
psync.py -p "$TM_PROJECT_FILEPATH" (in TextMate)

For the -p switch examples, note that this only works if files for that project live in $SANDBOX/project_name_without_extension/, i.e. ~/Sites/my_project/ in above

kumar.mcmillan/ 
gmail.com if you have questions

"""

import os
import sys
import commands
from optparse import OptionParser

class SyncException(Exception): pass
class IncorrectUsage(SyncException): pass

class PSync:
    """project sync tool"""
    
    def __init__(self, options):
        toload= [   'delete', 'directory', 'filename', 'hostname', 'project_filename', 
                    'sandbox_local', 'sandbox_remote', 'test', 'username']
        for key in toload:
            setattr(self, key, getattr(options, key))
        
        self.syncpath = None
        self.syncpath_basename = None
        
        if self.username is None:
            if os.getenv('USER') is not None:
                self.username = os.getenv('USER')
            else:
                raise IncorrectUsage("User option was empty and no $USER in env.")
        
        # setup sandbox :
        if self.sandbox_local is None:
            self.sandbox_local = '~/public_html'
            
            if str(commands.getoutput('hostinfo')).find('Darwin ') is not -1:
                self.sandbox_local = '~/Sites'
        if self.sandbox_local.endswith('/'):
            self.sandbox_local = self.sandbox_local[0:-1]
            
        self.sandbox_local = os.path.expanduser(self.sandbox_local)
        
        # setup paths :
        if self.filename:
            self.setPathsFromFile(self.filename)
        elif self.directory:
            self.setPathsFromDir(self.directory)
        elif self.project_filename: 
            self.setPathsFromProject()
        else:
            self.syncpath = self.sandbox_local + '/'
    
    def initSyncFromFile(self, filename):
        """common settings when syncing a file"""
        if filename[0]=='/':
            filename = filename[1:]
        self.syncpath_basename = filename
        self.syncpath = os.path.join(self.sandbox_local, self.syncpath_basename)
        if not os.path.exists(self.syncpath):
            raise IncorrectUsage(   "cannot sync by filename/directory.  "
                                    "local path '%s' does not exist" % self.syncpath)
        
    def rsync(self):
        """rsyncs local sandbox to remote sandbox"""
        sync_from = self.syncpath
        sync_to = '%s@%s:%s' % (self.username, self.hostname, self.sandbox_remote)
        
        if self.syncpath_basename is not None:  
            sync_to += '/' + self.syncpath_basename
        
        rsync = [   'rsync', '-auv', '--exclude=.svn', '--exclude="*.egg"', '--exclude="*.egg-info"',
                    '--exclude=CVS', '--exclude=.DS_Store', '--include="*.pyc"']
        
        if self.delete:
            rsync.extend( ['--delete'] )
        if self.test:
            rsync.extend( ['--dry-run'] )
            
        rsync.extend([sync_from, sync_to])
        cmd = ' '.join(rsync)
        
        if self.test:   
            print "DRY RUNNING: ",
        print cmd
        
        sys.exit(os.system(cmd))
            
    def setPathsFromDir(self, filename):
        self.initSyncFromFile(filename)
        if not os.path.isdir(self.syncpath):
            raise IncorrectUsage(   "cannot sync by directory, "
                                    "file '%s' is not a directory" % self.syncpath)
        self.syncpath += '/'
            
    def setPathsFromFile(self, filename):
        self.initSyncFromFile(filename)
        if not os.path.isfile(self.syncpath):
            raise IncorrectUsage(   "cannot sync by filename, "
                                    "file '%s' is not a file" % self.syncpath)
            
    def setPathsFromProject(self):
        """finds directory to rsync from module/branch """
            
        filename = os.path.basename(self.project_filename)
        parts = filename.split('.')[:-1]
        
        if len(parts) < 1:
            raise IncorrectUsage(   "expected project file, '%s', "
                                    "to end in dot tmproj (or any other extension)" % filename)
        self.syncpath_basename = '.'.join(parts)
        self.syncpath = self.sandbox_local + '/' + self.syncpath_basename + '/'
        if not os.path.exists(self.syncpath):
            raise IncorrectUsage("the assumed path, '%s', for project, '%s', "
                                    "does not exist" % \
                                            (self.syncpath, self.project_filename))

def main():
    (parser, options, args) = parse_args()
    
    try:
        path, = args
    except ValueError:
        pass
    else:
        hostname, options.directory = os.path.split(path)
        if not hostname:
            hostname = options.hostname
        else:
            options.hostname = hostname
            
    try:
        p = PSync(options)
        p.rsync()
    except IncorrectUsage, e:
        parser.error(e)

def parse_args():
    parser = OptionParser(usage="%prog [options] \n"
                         "       %prog [options] local_dir_to_sync \n"
                         "       %prog [options] hostname/local_dir_to_sync")
    parser.add_option("-a", "--all",
                      action="store_true",
                      dest="sync_all",
                      help="Sync all projects in sandbox (when run with no options, this happens)")
    parser.add_option("-d", "--directory",
                      action="store",
                      type="string",
                      help="Sync directory to sandbox (path must be relative to sandbox)")
    parser.add_option("-D", "--delete",
                      action="store_true",
                      help= "Delete files from remote host that do not exist on local host.  "
                            "Use with caution (like, only on your main workstation).")
    parser.add_option("-f", "--filename",
                      action="store",
                      type="string",
                      help="Sync filename to sandbox (path must be relative to sandbox)")
    parser.add_option("-l", "--sandbox_local",
                      action="store",
                      type="string",
                      help= "Path to local sandbox, tilde expands to home "
                            "(defaults to ~/Sites on Mac or ~/public_html otherwise)")
    parser.add_option("-r", "--sandbox_remote",
                      action="store",
                      type="string",
                      default='~/work',
                      help= "Path to remote sandbox, tilde expands to home "
                            "(defaults to ~/work)")
    parser.add_option("-H", "--hostname",
                      action="store",
                      type="string",
                      default='dev2',
                      help="Remote hostname (defaults to 'dev2' because I said so)")
    parser.add_option("-u", "--username",
                      action="store",
                      type="string",
                      help="Remote user name (defaults to $USER)")
    parser.add_option("-p", "--project",
                      action="store",
                      type="string",
                      dest="project_filename",
                      help= "Syncs a directory magically determined by PROJECT_FILENAME "
                            "(hint: something.trunk.tmproj=$SANDBOX/something.trunk/)")
    parser.add_option("-t", "--test",
                      action="store_true",
                      help="Send --dry-run flag to rsync (i.e. show what would happen)")
                  
    (options, args) = parser.parse_args()
    return (parser, options, args)

if __name__ == '__main__':
    main()
