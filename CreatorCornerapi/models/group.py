from django.db import models
from django.db.models.deletion import CASCADE

class Group(models.Model):
    '''Groups Model'''
    title = models.CharField(max_length=30)
    description = models.TextField()
    timestamp = models.DateField(auto_now=True)
    creator = models.ForeignKey("Creator", on_delete=CASCADE)
