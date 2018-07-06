from django.core.management.base import BaseCommand, CommandError
from tutorbot.models import Question as Question, Answer as Answer
from tutorbot.scrapers import scraper

# ref: https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'Collects knowledge from external sources in Q/A'

    def handle(self, *args, **options):
        count = 0
        self.stdout.write('Starting knowledge gathering...')
        qa_list = scraper.scrape()
        for qa in qa_list:
            qs = Question.objects.filter(text=qa['question'])
            self.stdout.write(qa['question'])
            if not qs:
                answer = Answer(summary=scraper.summarize(qa['answer']), text=scraper.get_text(qa['answer']), detail=qa['answer'], source=qa['source'])
                answer.save()
                question = Question(text=qa['question'], answer=answer)
                question.save()
                count += 1
            else:
                self.stdout.write(self.style.NOTICE('Skipping existing question: [%s]' % qa['question']))

        self.stdout.write(self.style.SUCCESS('Knowledge gathering complete. Found %d new knowledge items!' % count))
