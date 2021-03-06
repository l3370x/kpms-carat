from lesson.models import Lesson
from django.contrib import admin

class LessonAdmin(admin.ModelAdmin):
    fieldsets = [
	('Class Title', {'fields': ['title']}),
	('classes', {'fields': ['classes']}),
	('Lesson Number', {'fields': ['lessonNumber']}),
    ('webPage', {'fields': ['htmlStuff']}),
  ]

admin.site.register(Lesson, LessonAdmin)

