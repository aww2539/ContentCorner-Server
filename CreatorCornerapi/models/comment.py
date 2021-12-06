from django.db import models
from django.db.models.deletion import CASCADE

class Comment(models.Model):
    '''Comments Model'''
    post = models.ForeignKey("Post", on_delete=CASCADE, related_name="comments")
    user = models.ForeignKey("Creator", on_delete=CASCADE)
    body = models.TextField(max_length=300)
    timestamp = models.DateField(auto_now=True)
