
from django.core.management.base import BaseCommand, CommandError
from tutorbot.models import Question as Question, Answer as Answer
from chatterbot.ext.django_chatterbot.models import Statement
import json

similar_q_prefix_pairs = [
    ['what do you understand by', 'what is'],
    ['explain how', 'how'],
    ['explain what', 'what'],
]

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
                q_texts = self.create_similar_questions(q.text)
                # print ("----")
                for q_text in q_texts:
                    # print (q_text)
                    chatterbot.train([q_text, q.answer.summary])
                # print ("----")
                self.update_answer_statement_data(q.answer, q.answer.summary)
                q.learned=True
                q.save()
                count += 1

        self.stdout.write(self.style.SUCCESS('Knowledge learning complete. Found %d new knowledge items!' % count))

    def create_similar_questions(self, text):
        for q_prefix in similar_q_prefix_pairs:
            if text.lower().startswith(q_prefix[0]):
                list = []
                return [text, text.lower().replace(q_prefix[0], q_prefix[1], 1)]
        return [text]

    def update_answer_statement_data(self, answer, answer_summary):
        statement_qs = Statement.objects.filter(text=answer_summary)
        if statement_qs:
            statement = statement_qs[0]
            statement.extra_data = json.dumps({ 'answer': answer.id })
            statement.save()
        else:
            self.stdout.write(self.style.NOTICE('Couldn\'t save answer statement for [%s]' % answer_summary))
