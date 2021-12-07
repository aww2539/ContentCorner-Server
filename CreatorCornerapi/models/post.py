from django.db import models
from django.db.models.deletion import CASCADE

class Post(models.Model):
    '''Posts Model'''
    creator = models.ForeignKey("Creator", on_delete=CASCADE)
    group = models.ForeignKey("Group", on_delete=CASCADE)
    category = models.ForeignKey("Category", on_delete=CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    timestamp = models.DateField(auto_now=True)
