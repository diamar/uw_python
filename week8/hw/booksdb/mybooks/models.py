from django.db import models

class Poll(models.Model):
    bkid = models.CharField(max_length=5)
    title = models.CharField(max_length=500)
    isbn = models.CharField(max_length=25)
    publisher = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    def __unicode__(self):
        return self.bkid
    def __unicode__(self):
        return self.title
    def __unicode__(self):
        return self.isbn
    def __unicode__(self):
        return self.publisher
    def __unicode__(self):
        return self.author

