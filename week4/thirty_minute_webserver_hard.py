#
# ws30 -- the thirty minute web server
# author: Wilhelm Fitzpatrick (rafial@well.com)
# date: August 3rd, 2002
# version: 1.0
#
# Written after attending a Dave Thomas talk at PNSS and hearing about
# his "write a web server in Ruby in one hour" challenge.
#
# Actual time spent:
#  30 minutes reading socket man page
#  30 minutes coding to first page fetched
#   3 hours making it prettier & more pythonic
#
# updated for UW Internet Programming in Python, by Brian Dorsey
#

import os, socket, sys
import time
import datetime

defaults = ['127.0.0.1', '8080']
mime_types = {'.jpg' : 'image/jpg', 
             '.gif' : 'image/gif', 
             '.png' : 'image/png',
             '.html' : 'text/html', 
             '.pdf' : 'application/pdf'}
response = {}

response[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

response[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

response[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

DIRECTORY_LISTING =\
"""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""

DIRECTORY_LINE = '<a href="%s">%s</a><br>'

DATE_TIME =\
"""<html>
<head><title>Current Date and Time</title></head>
<body>
<a>The current date and time is %s </a><br>
</body>
</html>
""" % datetime.datetime.now()

runpyfile =\
"""<html>
<head><title>from py file</title></head>
<body>
<a> %s </a><br>
</body>
</html>
""" % pyfile
          

def exec_py(pyfile):
    import pyfile
    

def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    return s

def listen(s):
    connection, client = s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method = None
    while True:
        line = stream.readline()
        #print 'ABOUT TO PRINT line from get_request'
        #print line
        if not line.strip(): 
            break
        elif not method: 
            method, uri, protocol = line.split()
            #print 'ABOUT TO PRINT method, uri, protocol'
            #print method, uri, protocol  #uri is the path entered after host:8080, so like '/' or
                                        # '/date.html'
    return uri

def list_directory(uri):
    entries = os.listdir('.' + uri)
    entries.sort()
    return DIRECTORY_LISTING % (uri, uri, '\n'.join(
        [DIRECTORY_LINE % (e, e) for e in entries]))

def get_file(path):
    f = open(path)
    try: 
        return f.read() #reads and returns the entire contents of the file
    finally: 
        f.close()

def get_content(uri):
    print 'fetching:', uri
    try:
        path = '.' + uri
        print 'ABOUT TO PRINT path from get_content'
        print path
        if os.path.isfile(path):
            return (200, get_mime(uri), get_file(path))
        if path == './date.html':
            return (200, 'text/html', DATE_TIME)
        if uri.endswith('.py'):
            exec_py(path)
            return (200, 'text/html', runpyfile)
        if os.path.isdir(path):
            if(uri.endswith('/')):
                return (200, 'text/html', list_directory(uri)) #returns the file directory
            else:
                return (301, uri + '/')
        else: return (404, uri)
    except IOError, e:
        return (404, e)

def get_mime(uri): #returning the type of file, from the dictionary it returns the value.
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain') #splitext gets the extension,
                                            #if the extention is not found in mime_types dic,
                                            #then it returns the default 'text\plain'

def send_response(stream, content):
    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            stream = listen (server)
            print stream
            send_response(stream, get_content(get_request(stream)))
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()

