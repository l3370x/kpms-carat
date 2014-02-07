from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
                        {'template_name': 'student/login.html'}),
	url(r'^oauth2callback', 'student.views.auth_return'),
	url(r'^$', 'student.views.index'),
)
