from django.db import models
import datetime

# Create your models here.

class Poll(models.Model):
    # telling Django that the filed name will be
    # 'question' and the field type will be 'CharField'
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.question
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'


class Choice(models.Model):
    # note a relationship is defined, using ForeignKey.
    # That tells Django each Choice is related to a single Poll.
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    def __unicode__(self):
        return self.choice
