"""

A script to scrape QandA transcripts. Because you're a sucker for punishment.

patrick-dd.github.io
twitter.com/patrickdoupe
"""
import sys
sys.setrecursionlimit(2500)
import re
import requests
from bs4 import BeautifulSoup

class qanda_scraper:

    def __init__(self, html_link, filename):
        self.html_link = html_link
        self.filename = filename

    def download_page(self):
        """
        inputs:
            html_link: string
        outputs:
            unedited_transcript: string
        """
        page = requests.get(self.html_link)
        if page.status_code!=requests.codes.ok:
            pass
        else:
            # downloaded page
            soup = BeautifulSoup(page.text, 'html.parser')
            self.transcript = str(soup.find(id="transcript"))
        return 0

    def transcript_cleaner(self):
        """
        input:
            transcript: string
        output:
            edited_transcript: string
        """
        cleanr = re.compile('<.*?>')
        self.transcript = re.sub(cleanr, '', self.transcript)
        self.transcript = self.transcript.replace("\r\n\t","")
        return 0 

if __name__=="__main__":
    filename = 'qanda_transcripts.txt'
    html_links_file = 'qanda_episodes.txt'
    # getting links, last element is '\n' so removing it
    html_links = open(html_links_file, 'r').read().split(',')[:-1]
    # getting unique links
    html_links = list(set(html_links))
    transcript = ''
    print 'Downloading transcripts'
    for link in html_links:
        print 'Downloading transcript from website ' + link.strip()
        qanda = qanda_scraper(link.strip(), filename)
        qanda.download_page()
        qanda.transcript_cleaner()
        transcript += qanda.transcript
    
    f = open(filename, 'w')
    f.write(transcript)
    f.close()
    print 'Transcript saved'
