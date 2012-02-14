"""
Demonstrate screen scraping with BeautifulSoup 

Installed from http://www.crummy.com/software/BeautifulSoup/#Download/ 
Explained at http://www.crummy.com/software/BeautifulSoup/documentation.html
"""

import urllib2
import urllib
import re
from pprint import pprint
from BeautifulSoup import BeautifulSoup

# read a web page into a big string
webpage = 'http://jon-jacky.github.com/uw_python/winter_2012/index.html'
page = urllib2.urlopen('http://jon-jacky.github.com/uw_python/winter_2012/index.html').read()

# parse the string into a "soup" data structure
soup = BeautifulSoup(page)

# find all the anchor tags that link to Python files
pythonfiles = soup.findAll('a',attrs={'href':(lambda a: a and a.endswith('.py'))})
print pythonfiles

repository = 'http://jon-jacky.github.com/uw_python/winter_2012/'
outdir = '/Users/AtHome/uw_python/week5/downloads/'

for pyfile in pythonfiles:
    strpyfile = str(pyfile)
    dwlfile = repository + strpyfile.split('"')[1]
    outfile = outdir + strpyfile.split('"')[1].split('/')[-1]
    urllib.urlretrieve(dwlfile, outfile)
    
    
