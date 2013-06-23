from django.conf.urls.defaults import *

urlpatterns = patterns('teacher.views',
			url(r'^teacher/$', 'teacherHome'),
			url(r'^addStudent/$', 'addStudent'),
			url(r'^allStudents/$', 'allStudents'),
			url(r'^student/(?P<usern>\w+)/$', 'studentInfo'),
			url(r'^student/(?P<usern>\w+)/changePassword$', 'studentPassChange'),
			url(r'^student/(?P<usern>\w+)/changeInfo$', 'studentInfoChange'),
			url(r'^$', 'teacherHome'),
			)
