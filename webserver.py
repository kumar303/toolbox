#!/usr/bin/env python
"""Run this script to start a small web server that will serve the test files.
"""

import optparse
import logging, time, os
from wsgiref import simple_server
log = logging.getLogger(__name__)
document_root = None

def fileapp(environ, start_response):
    path_info = environ['PATH_INFO']
    if path_info.startswith('/'):
        path_info = path_info[1:] # make relative
    full_path = os.path.join(document_root, path_info)
    if full_path == '':
        full_path = '.' # must be working dir
    if path_info=="" or path_info.endswith('/') or os.path.isdir(full_path):
        # directory listing:
        out = ['<html><head></head><body><ul>']
        for filename in os.listdir(full_path):
            if filename.startswith('.'):
                continue
            if os.path.isdir(os.path.join(full_path, filename)):
                filename = filename + '/'
            out.append('<li><a href="%s">%s</a></li>' % (filename, filename))
        out.append("</ul></body></html>")
        
        body = "".join( out )
    else:
        f = open(full_path, 'r')
        body = f.read() # optimized for small files :)
    
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(body)))])
    return [body]
    
def main():
    global document_root
    p = optparse.OptionParser(usage="%prog")
    p.add_option("--port", help="Port to run server on.  Default: %default", default=8090, type=int)
    p.add_option("--directory", help="Directory to serve files from. Defaults to working directory.", default=os.getcwd())
    (options, args) = p.parse_args()
    document_root = options.directory
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(message)s')
    log.info("starting test server on port %s", options.port)
    log.info("serving files in %s", options.directory)
    httpd = simple_server.WSGIServer(('', options.port), simple_server.WSGIRequestHandler)
    httpd.set_app(fileapp)
    httpd.serve_forever()

if __name__ == '__main__':
    main()