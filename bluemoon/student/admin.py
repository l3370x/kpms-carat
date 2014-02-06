from student.models import Student
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
  fieldsets = [
	('User Info', {'fields': ['user']}),
	('oauth token', {'fields': ['oauth_token']}),
	('oauth secret', {'fields': ['oauth_secret']}),
  ]
  readonly_fields = ('user',)

admin.site.register(Student, StudentAdmin)

