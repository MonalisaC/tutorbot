from __future__ import print_function
import urllib2
from stackapi import StackAPI, StackAPIError
from bs4 import BeautifulSoup
from tutorbot.collectors.base import BaseCollector
import time

# ref - http://stackapi.readthedocs.io/en/latest/index.html

class Stacker(BaseCollector):

    def __init__(self):
        self.tags = ['javascript','react','redux','react-redux','ruby','ruby-on-rails'] # stackoverflow tags based on details from https://stackoverflow.com/tags
        self.min_score = 200 # https://meta.stackexchange.com/questions/229255/what-is-the-score-of-a-post
        self.site_name = 'stackoverflow'

    def collect(self):
        qa_list = []
        try:
            site = StackAPI(self.site_name)
            site.page_size = 10
            site.max_pages = 1
            # calling fetch with various parameters - http://stackapi.readthedocs.io/en/latest/user/advanced.html#calling-fetch-with-various-api-parameters
            questions = site.fetch('questions', min=self.min_score, tagged=self.tags, sort='votes', accepted='True')
            while (self.wait_if_throttled(questions)):
                questions = site.fetch('questions', min=self.min_score, tagged=self.tags, sort='votes', accepted='True')
            print ('No of questions from %s = %d' % (self.site_name, len(questions['items'])))
            for q in questions['items']:
                time.sleep(1/25) # this is to ensure less than 30 req per second (https://api.stackexchange.com/docs/throttle)
                if 'accepted_answer_id' in q.keys():
                    question = q['title']
                    tags = q['tags']
                    aa = site.fetch('posts', ids=[q['accepted_answer_id']])
                    while (self.wait_if_throttled(aa)):
                        aa = site.fetch('posts', ids=[q['accepted_answer_id']])
                    answer_link = aa['items'][0]['link']
                    answer = self.extract_accepted_answer_post(answer_link)
                    scraped = {'question': question, 'answer': answer, 'source':answer_link, 'tags': tags}
                    # print scraped
                    # print question
                    qa_list.append(scraped)
                    self.add_qa(scraped)
        except StackAPIError as e:
            print('Failed to fetch data from stack overflow: [%s]. Skipping.' % e.message)
        return qa_list

    def extract_accepted_answer_post(self, link):
        page = urllib2.urlopen(link)
        soup = BeautifulSoup(page, 'html.parser')
        # accepted_answer = soup.find('div', {'itemprop' == 'acceptedAnswer'})
        accepted_answer = soup.select('div[itemprop="acceptedAnswer"]')[0]
        accepted_answer_post = accepted_answer.select('div[class="post-text"]')[0]
        return str(self.remove_all_span(self.remove_all_attrs_except(accepted_answer_post)))

    def wait_if_throttled(self, result):
        ''' Checks if the result has a backoff and if so sleeps for that long and returns true. Else (if not throttled) returns false.
            Based on details in https://api.stackexchange.com/docs/throttle. '''
        backoff = result.get('backoff', 0)
        if backoff > 0:
            print('Backing off for %d seconds' %s)
            time.sleep(backoff)
            return True
        return False