from django.conf.urls.defaults import *

urlpatterns = patterns('student.views',
			url(r'^student/$', 'startPage'),
			url(r'^$', 'startPage'),
			url(r'^auth/login/$', 'login'),
			url(r'^auth/logout/$', 'logout'),
			)
