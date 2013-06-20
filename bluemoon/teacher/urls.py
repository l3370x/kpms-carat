from django.conf.urls.defaults import *

urlpatterns = patterns('teacher.views',
			url(r'^teacher/$', 'teacherHome'),
			url(r'^$', 'teacherHome'),
			)
