from django.conf.urls.defaults import *

urlpatterns = patterns('student.views',
			url(r'^$', 'index'),
		    url(r'^oauth2callback', 'auth_return')
			)
