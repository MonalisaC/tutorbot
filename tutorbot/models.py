from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

class Answer(models.Model):
    summary  = models.TextField(max_length=1000)
    text     = models.TextField(max_length=10000)
    detail   = models.TextField(max_length=10000)
    source   = models.TextField(max_length=1000)
    created  = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    # reference: https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return self.summary.encode('ascii', 'ignore').decode('ascii')

    def serialize(self):
        """
        :returns: A dictionary representation of the answer object.
        :rtype: dict
        """
        import json
        data = {}

        data['summary'] = self.summary
        data['text'] = self.text
        data['detail'] = self.detail
        data['source'] = self.source
        return data

class Question(models.Model):
    text     = models.CharField(max_length=500)
    answer   = models.ForeignKey(Answer, on_delete=models.CASCADE)
    learned  = models.BooleanField(default=False)
    created  = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    tags     = TaggableManager()

    # reference: https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.text.encode('ascii', 'ignore').decode('ascii')
