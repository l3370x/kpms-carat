from django.conf.urls.defaults import *

urlpatterns = patterns('student.views',
			url(r'^student/$', 'studentHome'),
			url(r'^login/?$', 'google_login'),
		    url(r'^logout/?$', 'google_logout'),
		    url(r'^login/authenticated/?$', 'google_authenticated'),
			)
