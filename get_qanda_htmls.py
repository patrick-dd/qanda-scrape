import requests
from bs4 import BeautifulSoup
from __future__ import print_function

html_link = 'http://www.abc.net.au/tv/qanda/past-programs-by-date.htm'

page = requests.get(html_link)
soup = BeautifulSoup(page.text, 'lxml')

f = open('qanda_episodes.txt', 'w')

for link in soup.find_all('a'):
    if 'http://www.abc.net.au/tv/qanda/txt/' in link.get('href'):
        f.write(link.get('href'))
        f.write(', ')

f.close()
print( 'Websites scraped!' )



