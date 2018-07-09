from __future__ import print_function
import urllib2
from bs4 import BeautifulSoup, Tag
from string import digits
import re
from base import BaseCollector

class Scraper(BaseCollector):

    def __init__(self):
        self.source = 'https://www.edureka.co/blog/interview-questions/react-interview-questions/'

    def collect(self):
        page = urllib2.urlopen(self.source)
        soup = BeautifulSoup(page, 'html.parser')
        h3s = soup.find_all('h3')
        qa_list = []
        for h3 in h3s:
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
                scraped = {'question': question, 'answer': answer, 'source':self.source}
                # print(scraped)
                qa_list.append(scraped)
                self.add_qa(scraped)
        return qa_list