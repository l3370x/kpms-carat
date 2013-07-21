from student.models import Student
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
  fieldsets = [
	('User Info', {'fields': ['user']}),
	('first name', {'fields': ['first_name']}),
	('last name', {'fields': ['last_name']}),
	('email', {'fields': ['email']}),
    ('classes', {'fields': ['classes']}),
  ]
  readonly_fields = ('user',)

admin.site.register(Student, StudentAdmin)

