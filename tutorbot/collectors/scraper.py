from __future__ import print_function
import urllib2
from bs4 import BeautifulSoup, Tag
from string import digits
import re
from base import BaseCollector

class Scraper(BaseCollector):

    def __init__(self):
        self.source = 'https://www.edureka.co/blog/interview-questions/react-interview-questions/'
        self.tags = ['react']

    def collect(self, *args, **options):
        page = urllib2.urlopen(self.source)
        soup = BeautifulSoup(page, 'html.parser')
        h3s = soup.find_all('h3')
        qa_list = []
        total = len(h3s)
        print('Collecting from %s' % self.source)
        processed = 0
        added = 0
        skipped = 0
        for h3 in h3s:
            processed += 1
            text = h3.get_text()
            if text[0].isdigit():
                question = text.lstrip(digits).lstrip('.').strip()
                answer = ""
                next = h3.next_sibling
                while(True):
                    while(not isinstance(next, Tag) and next != None):
                        next = next.next_sibling
                    if next == None or next.name == 'h3':
                        break;
                    else:
                        answer = answer + str(self.remove_all_span(self.remove_all_attrs_except(next))) #.prettify()
                        if next.name != 'p':
                            break
                        next = next.next_sibling
                answer = '<div>' + answer + '</div>'
                scraped = {'question': question, 'answer': answer, 'source':self.source, 'tags': self.tags }
                # print(scraped)
                qa_list.append(scraped)
                if self.add_qa(scraped):
                    added += 1
                else:
                    skipped += 1
            self.show_progress(processed, total, added, skipped)
        return qa_list
