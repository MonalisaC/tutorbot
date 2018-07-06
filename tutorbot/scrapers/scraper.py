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
            # print(scraped)
            qa_list.append(scraped)
    return qa_list

def get_text(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

def summarize(html_text):
    # For now this is just 1st line if available. Maybe TODO: come up with a better technique!
    soup = BeautifulSoup(html_text, 'html.parser')
    lines = soup.get_text().strip().split('\n')
    summary = lines[0].split('.')[0].strip() if len(lines) > 0 else ''
    return summary

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
