from django.core.management.base import BaseCommand, CommandError
from tutorbot.models import Question as Question, Answer as Answer

# ref: https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'Learns from gathered new knowledge'

    def handle(self, *args, **options):
        from chatterbot import ChatBot
        from chatterbot.ext.django_chatterbot import settings
        from chatterbot.trainers import ListTrainer

        chatterbot = ChatBot(**settings.CHATTERBOT)
        chatterbot.set_trainer(ListTrainer)

        count = 0
        qs = Question.objects.filter(learned=False)
        if not qs:
            self.stdout.write(self.style.NOTICE('No new questions to learn!'))
        else:
            self.stdout.write('Found new questions. Learning!')
            for q in qs:
                qs = Question.objects.filter(text=q.text)
                chatterbot.train([q.text, q.answer.text])
                q.learned=True
                q.save()
                count += 1

        self.stdout.write(self.style.SUCCESS('Knowledge learning complete. Found %d new knowledge items!' % count))
