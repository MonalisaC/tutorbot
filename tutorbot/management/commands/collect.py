from django.core.management.base import BaseCommand, CommandError
from tutorbot.models import Question as Question, Answer as Answer
from tutorbot.collectors.scraper import Scraper

# ref: https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'Collects knowledge from external sources in Q/A format'

    def handle(self, *args, **options):
        count = 0
        self.stdout.write(self.style.NOTICE('Starting knowledge gathering...'))
        start = Question.objects.count()
        scraper = Scraper()
        scraper.collect()
        end = Question.objects.count()
        self.stdout.write(self.style.SUCCESS('Knowledge gathering complete. Found %d new knowledge items!' % (end - start)))
