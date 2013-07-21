from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe

from course.models import *

class Lesson(models.Model):
    def __unicode__(self):
        return self.title
    title = models.CharField(max_length = 200)
    classes = models.ManyToManyField(Class)
    date = models.DateField(blank = True)
    htmlStuff = models.TextField(blank = True)

    def display_safeHTML(self):
        return mark_safe(self.htmlStuff)

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        widgets = {
          'htmlStuff': forms.Textarea(attrs = {'rows':40, 'cols':15}),
        }
        exclude = ('classes', 'date')
