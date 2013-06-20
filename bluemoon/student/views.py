from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render

from student.models import *
from teacher.models import *

ADMIN_NAME = 'l3370x'
TEACHER_USERNAME = 'Rick'

def startPage(request):
	if request.user.is_authenticated():
		if request.user.username == ADMIN_NAME:
			logout(request)
			return login(request)
		if request.user.username == TEACHER_USERNAME:
			return teacherHome(request)
		return studentHome(request)
	return login(request)

def teacherHome(request,teacherUser):
	theTeacher = Teacher.objects.get(user=teacherUser.id)
	return render(request,'teacher/teacherHome.html',{'theTeacher':theTeacher})

def logout(request):
	django.contrib.auth.logout(request)
	return startPage(request)

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('auth/login.html', {'form':form},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render_to_response('auth/login.html', {'form':form},
                                  context_instance=RequestContext(request))

        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render_to_response('auth/login.html',
                                      {'form':form,
                                       'error': 'Invalid username or password'},
                                      context_instance=RequestContext(request))
        if user.username == TEACHER_USERNAME:
			return teacherHome(request,user)
        django.contrib.auth.login(request,user)
        return studentHome(request)

def studentHome(request):
	theStudent = Student.objects.get(user=request.user.id)
	return render(request,'student/studentHome.html', {'theStudent':theStudent})
