from course.models import Class
from django.contrib import admin

class ClassAdmin(admin.ModelAdmin):
    fieldsets = [
	('Class Title', {'fields': ['class_title']}),
	('calendar url', {'fields': ['calendar_url']}),
	('notes', {'fields': ['notes']}),
  ]

admin.site.register(Class, ClassAdmin)

