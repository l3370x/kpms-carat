from django.db import models
from django.contrib.auth.models import User
from django import forms

class Teacher(models.Model):
  def __unicode__(self):
    return self.first_name
  user = models.ForeignKey(User, editable = False)
  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  email = models.EmailField()

class TeacherForm(forms.ModelForm):
  class Meta:
    model = Teacher
