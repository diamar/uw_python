"""
From Brian Dorsey's Internet Programming in Python, Winter 2011
"""

import bookdb

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
        print id
        print title
        bksindexpage = bksindexpage + '<p><a href:"localhost:8080/%s.html"> %s </a></p>' % (id, title)
        counter += 1
    return bksindexpage

print ind_book_info('id2')
print mk_index()
