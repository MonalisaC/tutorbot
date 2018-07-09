from bs4 import BeautifulSoup, Tag
from tutorbot.models import Question as Question, Answer as Answer

class BaseCollector(object):

    def get_text_from_html(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()

    def summarize_html(self, html_text):
        # For now this is just 1st line if available. Maybe TODO: come up with a better technique!
        soup = BeautifulSoup(html_text, 'html.parser')
        lines = soup.get_text().strip().split('\n')
        summary = lines[0].split('.')[0].strip() if len(lines) > 0 else ''
        return summary

    def remove_all_attrs_except(self, soup):
        whitelist = ['a','img']
        for tag in soup.find_all(True):
            if tag.name not in whitelist:
                tag.attrs = {}
        return soup

    def remove_all_span(self, soup):
        for match in soup.findAll('span'):
            match.unwrap()
        return soup

    def add_qa(self, qa):
        qs = Question.objects.filter(text=qa['question'])
        if not qs:
            answer = Answer(summary=self.summarize_html(qa['answer']), text=self.get_text_from_html(qa['answer']), detail=qa['answer'], source=qa['source'])
            answer.save()
            question = Question(text=qa['question'], answer=answer)
            question.save()
        else:
            # self.stdout.write(self.style.NOTICE('Skipping existing question: [%s]' % qa['question']))
            print('Skipping existing question: [%s]' % qa['question'])