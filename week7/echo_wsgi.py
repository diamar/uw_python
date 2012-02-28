"""
Minimal WSGI + forms demo, with persistence

Send HTML page that echoes message from HTTP request
To get started, point browser at echo_wsgi.html

Based on example in PEP 333, then add path and query processing
"""

import urlparse
import bookdb

# send one of these pages, depending on URL path

form_page = """<head>
<title>Echo request</title>
</head>
<body>
<form method="GET" action="echo_wsgi.py">
Message: <input type="text" name="message" size="40">
<input type="submit" value="Submit">
</form>
</body>
</html>
"""

#message_template = """
#<html>
#<head>
#<title>Echo response</title>
#</head>
#<body>
#Message: %s
#</form>
#</body>
#</html>
#"""
message_template = """
<html>
<head>
<title>Echo response</title>
</head>
<body>
%s
</form>
</body>
</html>
"""
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

global myvar
myvar = []


def test_list_books():
    books = bookdb.BookDB()
    titles = books.titles()
    assert len(titles) > 1
    print titles
    for title in titles:
        assert 'title' in title
        assert 'id' in title

def test_get_book_info():
    books = bookdb.BookDB()
    titles = books.titles()
    id = titles[0]['id']
    print id
    info = books.title_info(id)
    print info
    assert 'title' in info
    assert info['title'] == titles[0]['title']
    assert 'publisher' in info
    assert 'isbn' in info
    assert 'author' in info

def book_info():
    books = bookdb.BookDB()
    titles = books.titles()
    numbooks = len(titles)
    counter = 0
    while counter < numbooks:
        id = titles[counter]['id']
        print id
        info = books.title_info(id)
        print info
        counter += 1

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
    if path == '/echo_wsgi.html':
        page = form_page
    elif path == '/index.html':
        page = index % mk_index()
    elif path == '/getbook':
        #bookid = urlparse.parse_qs(environ['QUERY_STRING'])['message'][0]
        bookid = environ['QUERY_STRING']
        print bookid
        page = book_information % ind_book_info(bookid)
    elif path == '/echo_wsgi.py':
        # get message from URL query string, parse_qs returns a list for each key
        #page = message_template % (
        #    urlparse.parse_qs(environ['QUERY_STRING'])['message'][0])
        print urlparse.parse_qs(environ['QUERY_STRING'])['message'][0]
        myvar.append(urlparse.parse_qs(environ['QUERY_STRING'])['message'][0])
        print myvar
        str2rtn = ''
        for var in myvar:
            str2rtn = str2rtn +"<P> Message: "+ var + "</P>"
        page = message_template % str2rtn    
    else:
        page = notfound_template % path
    return [ page ] # list of strings - must return iterable, not just a string
