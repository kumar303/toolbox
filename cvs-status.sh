#!/bin/bash

# does a cvs status like svn status :
cvs status 2>&1 | egrep "(^\? |Status: )" | grep -v Up-to-date