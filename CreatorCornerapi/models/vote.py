from django.db import models
from django.db.models.deletion import CASCADE

class Vote(models.Model):
    '''Votes Model'''
    user = models.ForeignKey("Creator", on_delete=CASCADE)
    post = models.ForeignKey("Post", on_delete=CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)
