"""
Minimal WSGI + forms demo, with persistence

Send HTML page that echoes message from HTTP request
To get started, point browser at bookdb_wsgi.html

Based on example in PEP 333, then add path and query processing
"""

import urlparse
import bookdb

# send one of these pages, depending on URL path

index = """
<html>
<head>
<title>Index</title>
</head>
<body>
%s
</form>
</body>
</html>
"""

book_information = """
<html>
<head>
<title>Book Information</title>
</head>
<body>
%s
</form>
</body>
</html>
"""

notfound_template = """
<html>
<head>
<title>404 Not Found</title>
</head>
<body>
404 %s not found
</form>
</body>
</html>
"""

def ind_book_info(id):
    books = bookdb.BookDB()
    bookdic = books.title_info(id)
    bktitle = bookdic['title']
    bkisbn = bookdic['isbn']
    bkpublisher = bookdic['publisher']
    bkauthor = bookdic['author']
    infoaboutbook = '<P> Tittle: %s</P><P> ISBN: %s</P><P> Publisher: %s</P><P> Author: %s</P>' % (bktitle, bkisbn, bkpublisher, bkauthor) 
    return infoaboutbook

def mk_index():
    books = bookdb.BookDB()
    titles = books.titles()
    numbooks = len(titles)
    counter = 0
    bksindexpage = ''
    while counter < numbooks:
        id = titles[counter]['id']
        title = titles[counter]['title']
        #print id
        #print title
        bksindexpage = bksindexpage + '<p><a href="http://localhost:8080/getbook?%s"> %s </a></p>' % (id, title)
        counter += 1
    return bksindexpage

# must be named 'application' to work with our wsgi simple server
def application(environ, start_response): 
    status = '200 OK'
    response_headers = [('Content_type', 'text/HTML')]
    start_response(status, response_headers)
    # send different page depending on URL path
    path = environ['PATH_INFO']
    
    if path == '/index.html':
        page = index % mk_index()
    elif path == '/getbook':
        #bookid = urlparse.parse_qs(environ['QUERY_STRING'])['message'][0]
        bookid = environ['QUERY_STRING']
        print bookid
        page = book_information % ind_book_info(bookid)  
    else:
        page = notfound_template % path
    return [ page ] # list of strings - must return iterable, not just a string
