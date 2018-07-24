from __future__ import unicode_literals
from chatterbot.logic.logic_adapter import LogicAdapter
from chatterbot.logic.best_match import BestMatch
from taggit.models import Tag
from tutorbot.models import Question
from sets import Set

class TaggedBestMatch(BestMatch):
    """
    A logic adapter that extends BestMatch to use tags (if available) on questions
    and filter the statement list to find the closest matches to the input statement.
    """

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.chatbot.storage.get_response_statements()

        if not statement_list:
            if self.chatbot.storage.count():
                # Use a randomly picked statement
                self.logger.info(
                    'No statements have known responses. ' +
                    'Choosing a random response to return.'
                )
                random_response = self.chatbot.storage.get_random()
                random_response.confidence = 0
                return random_response
            else:
                raise self.EmptyDatasetException()

        # check for tags in the input statement
        tags = Tag.objects.all()
        tags_filter = []
        for tag in tags:
            if str(tag) in input_statement.text:
                tags_filter.append(tag)
        statement_text_filter = Set()
        confidence_boost = 1
        if len(tags_filter) > 0:
            questions = Question.objects.filter(tags__name__in=tags_filter)
            if questions:
                for q in questions:
                    statement_text_filter.add(q.text)

        closest_match = input_statement
        closest_match.confidence = 0

        # Find the closest matching known statement
        for statement in statement_list:
            if len(statement_text_filter) == 0 or statement.text in statement_text_filter:
                confidence_boost = 1.2
                confidence = self.compare_statements(input_statement, statement) * confidence_boost

                if confidence > closest_match.confidence:
                    statement.confidence = confidence
                    closest_match = statement

        return closest_match
