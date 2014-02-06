from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
  user = models.ForeignKey(User, editable = False)
  oauth_token = models.CharField(max_length = 200)
  oauth_secret = models.CharField(max_length = 200)
