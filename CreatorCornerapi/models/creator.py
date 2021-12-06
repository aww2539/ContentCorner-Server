from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Creator(models.Model):

    user = models.OneToOneField(User, on_delete=CASCADE)
