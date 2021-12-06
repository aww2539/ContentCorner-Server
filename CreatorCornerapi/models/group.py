from django.db import models

class Group(models.Model):
    '''Groups Model'''
    title = models.CharField(max_length=30)
    description = models.TextField()
    timestamp = models.DateField(auto_now=True)
