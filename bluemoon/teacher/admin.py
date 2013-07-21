from teacher.models import Teacher
from django.contrib import admin

class TeacherAdmin(admin.ModelAdmin):
  fieldsets = [
	('User Info', {'fields': ['user']}),
	('first name', {'fields': ['first_name']}),
	('last name', {'fields': ['last_name']}),
	('email', {'fields': ['email']}),
  ]
  readonly_fields = ('user',)

admin.site.register(Teacher, TeacherAdmin)

