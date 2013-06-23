from django.conf.urls.defaults import *

urlpatterns = patterns('student.views',
			url(r'^student/$', 'studentHome'),
			url(r'^allClasses/$', 'allClasses'),
			url(r'^class/(?P<classID>\d+)/$', 'classInfo'),
			url(r'^lesson/(?P<lessonID>\d+)/$', 'lessonPage'),
			url(r'^$', 'startPage'),
			url(r'^auth/login/$', 'login'),
			url(r'^auth/logout/$', 'logout'),
			)
