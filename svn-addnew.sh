#!/bin/sh

# adds any new files to the repository
# warning: you need to be diligent about svn:ignore !
# http://life.lukewarmtapioca.com/articles/trackback/33
svn status | grep "^\?" | awk '{print $2}' | xargs svn add