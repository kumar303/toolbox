#!/usr/bin/env python

"""Builds a widget using CONTENT_DIR as the source. 
Outputs to WIDGET_NAME.wdgt in current working directory.
Overwrites WIDGET_NAME.wdgt if it exists"""

from optparse import OptionParser
import os
import shutil

class Widget:
    def __init__(self, widgetDir, widgetName):
        self.contentDir = widgetDir
        self.name = widgetName
        
    def build(self, outputDir):
        outputTo = "%s/%s.wdgt" % (outputDir, self.name)
        
        if os.path.exists(outputTo):
            shutil.rmtree(outputTo)
        shutil.copytree(self.contentDir, outputTo)

if __name__ == '__main__':
    parser = OptionParser(usage="Usage: %prog [h] CONTENT_DIR WIDGET_NAME" + "\n\n" + __doc__)
    (options, args) = parser.parse_args()
    
    if len(args) != 2:
        parser.error('incorrect args')
    wdgt = Widget(args[0], args[1])
    wdgt.build(os.getcwd())