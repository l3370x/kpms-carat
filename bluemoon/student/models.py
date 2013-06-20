from django.db import models
from django.contrib.auth.models import User
from django import forms

class Student(models.Model):
  def __unicode__(self):
    return self.first_name
  user = models.ForeignKey(User,editable=False)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField()

class StudentForm(forms.ModelForm):
  class Meta:
    model = Student

class LoginForm(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)

class UserForm(forms.Form):
  username = forms.CharField(max_length=100)
  first_name = forms.CharField(max_length=50)
  last_name = forms.CharField(max_length=50)
  email = forms.CharField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
  confirm = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)

