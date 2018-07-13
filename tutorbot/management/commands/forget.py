from django.core.management.base import BaseCommand, CommandError
from chatterbot.ext.django_chatterbot.models import (Statement, Response, Conversation)
from tutorbot.models import Question as Question

# ref: https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'Forgets conversations, responses, and statements'

    def handle(self, *args, **options):
        Conversation.objects.all().delete()
        Response.objects.all().delete()
        Statement.objects.all().delete()
        qs = Question.objects.filter(learned=True)
        for q in qs:
            qs = Question.objects.filter(text=q.text)
            q.learned=False
            q.save()

        self.stdout.write(self.style.SUCCESS('Removed conversations, responses, and statements!'))
