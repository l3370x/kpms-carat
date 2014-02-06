from django.db import models
from django import forms

from lesson.models import *

class Question(models.Model):
    notes = models.TextField()
    lessons = models.ManyToManyField(Lesson)
