import urllib2
from bs4 import BeautifulSoup, Tag
from string import digits
import re

source = 'https://www.edureka.co/blog/interview-questions/react-interview-questions/'

def scrape():
    page = urllib2.urlopen(source)
    soup = BeautifulSoup(page, 'html.parser')
    h3s = soup.find_all('h3')
    qa_list = []
    for h3 in h3s:
        text = h3.get_text()
        if text[0].isdigit():
            question = text.lstrip(digits).lstrip('.').strip()
            print(question)
            answer = ""
            next = h3.next_sibling
            while(True):
                while(not isinstance(next, Tag) and next != None):
                    next = next.next_sibling
                if next == None or next.name == 'h3':
                    break;
                else:
                    answer = answer + str(_remove_all_span(_remove_all_attrs_except(next))) #.prettify()
                    if next.name != 'p':
                        break
                    next = next.next_sibling
            answer = '<div>' + answer + '</div>'
            scraped = {'question': question, 'answer': answer, 'source':source}
            print(scraped)
            qa_list.append(scraped)
    return qa_list

def _remove_all_attrs_except(soup):
    whitelist = ['a','img']
    for tag in soup.find_all(True):
        if tag.name not in whitelist:
            tag.attrs = {}
    return soup

def _remove_all_span(soup):
    for match in soup.findAll('span'):
        match.unwrap()
    return soup

def main():
    scrape()

if __name__ == "__main__":
    main()
