from django.core.management.base import BaseCommand, CommandError
from tutorbot.models import Question as Question, Answer as Answer
from tutorbot.collectors.scraper import scrapers
from tutorbot.collectors.stacker import Stacker

# ref: https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'Collects knowledge from external sources in Q/A format'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fromdate', dest='fromdate', help='from date in format YYYYMMDD', required=False)
        parser.add_argument('--todate', dest='todate', help='to date in format YYYYMMDD', required=False)
        parser.add_argument('--tagged', dest='tagged', help='comma separated tags', required=False)
        parser.add_argument('--min', dest='min', help='min score', required=False)
        parser.add_argument('--count', dest='count', help='count of questions', type=int, required=False)

    def handle(self, *args, **options):
        count = 0
        self.stdout.write(self.style.NOTICE('Starting knowledge gathering...'))
        start = Question.objects.count()
        for scraper in scrapers:
            scraper.collect(*args, **options)
        stacker = Stacker()
        stacker.collect(*args, **options)
        end = Question.objects.count()
        self.stdout.write(self.style.SUCCESS('Knowledge gathering complete. Found %d new knowledge items!' % (end - start)))
