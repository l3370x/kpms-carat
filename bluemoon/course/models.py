from django.db import models
from django import forms

class Class(models.Model):
    def __unicode__(self):
        return self.class_title
    class_title = models.CharField(max_length = 20)
    calendar_url = models.URLField(blank = True)
    notes = models.TextField(blank = True)



class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        exclude = ('lessons',)

class ClassNotesForm(forms.ModelForm):
    class Meta:
        model = Class
        exclude = ('class_title', 'calendar_url', 'lessons',)

class ClassTitleForm(forms.ModelForm):
    class Meta:
        model = Class
        exclude = ('notes', 'calendar_url', 'lessons',)
