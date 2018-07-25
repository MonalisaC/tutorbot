import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def get_conversation(self, request):
        """
        Return the conversation for the session if one exists.
        Create a new conversation if one does not exist.
        """
        from chatterbot.ext.django_chatterbot.models import Conversation, Response

        class Obj(object):
            def __init__(self):
                self.id = None
                self.statements = []

        conversation = Obj()

        conversation.id = request.session.get('conversation_id', 0)
        existing_conversation = False
        try:
            Conversation.objects.get(id=conversation.id)
            existing_conversation = True

        except Conversation.DoesNotExist:
            conversation_id = self.chatterbot.storage.create_conversation()
            request.session['conversation_id'] = conversation_id
            conversation.id = conversation_id

        if existing_conversation:
            responses = Response.objects.filter(
                conversations__id=conversation.id
            )

            for response in responses:
                conversation.statements.append(response.statement.serialize())
                conversation.statements.append(response.response.serialize())

        return conversation

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.read().decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        conversation = self.get_conversation(request)

        response = self.chatterbot.get_response(input_data, conversation.id)

        self.__add_or_update_extra_data(response)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        conversation = self.get_conversation(request)

        return JsonResponse({
            'name': self.chatterbot.name,
            'conversation': conversation.statements
        })

    def __add_or_update_extra_data(self, response):
        extra = response.extra_data
        # add answer data and more if there is some additional information available
        if isinstance(extra, basestring):
            try:
                extra = json.loads(extra)
                if 'answer' in extra:
                    from tutorbot.models import Answer
                    answer_obj = Answer.objects.get(pk=extra['answer'])
                    response.add_extra_data('answer_data', answer_obj.serialize())
                    self.__add_related_info(response, answer_obj)
            except ValueError:
                print("Ignoring extra")

        # add confidence
        response.add_extra_data('confidence', response.confidence)

    def __add_related_info(self, response, answer_obj):
        # get related questions for this answer (ref: https://stackoverflow.com/questions/15306897/django-reverse-lookup-of-foreign-keys)
        # and the get first form this queryset (ref: https://stackoverflow.com/questions/5123839/fastest-way-to-get-the-first-object-from-a-queryset-in-django)
        question = answer_obj.question_set.first()
        if question:
            related_qs = []
            q_tags = question.tags
            if q_tags:
                tags = []
                for q_tag in q_tags.names():
                    tags.append(str(q_tag))
            response.add_extra_data('tags', tags)
            q_objs = q_tags.similar_objects()
            for q_obj in q_objs:
                related_qs.append(q_obj.text)
            if len(related_qs) > 0:
                response.add_extra_data('related_questions', related_qs[:100])
