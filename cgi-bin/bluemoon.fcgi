#!/usr/bin/python
import sys, os

basepath = '/homepages/19/d429491612/htdocs'

sys.path.insert(0, basepath + '/.local/lib')
sys.path.insert(0, basepath + '/bluemoon')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bluemoon.settings'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method='threaded', daemonize='false')
