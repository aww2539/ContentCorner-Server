from django.db import models
from django.db.models.deletion import CASCADE

class CreatorGroup(models.Model):
    '''Model for Creators to join Groups'''
    creator = models.ForeignKey("Creator", on_delete=CASCADE)
    group = models.ForeignKey("Group", on_delete=CASCADE)
