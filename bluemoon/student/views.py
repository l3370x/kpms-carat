from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render

from student.models import *
from teacher.models import *
from teacher.views import *

def buildDict(s):
	d = {}
	d['theStudent'] = s
	d['myClasses'] = s.classes.all()
	return d

@login_required
def lessonPage(request, lessonID):
	try:
		theLesson = Lesson.objects.get(id = lessonID)
	except Lesson.DoesNotExist:
		raise Http404
	d = buildDict(Student.objects.get(user = request.user.id))
	d['theLesson'] = theLesson
	return render(request, 'student/lesson.html', d)

@login_required
def classInfo(request, classID):
	try:
		theClass = Class.objects.get(id = classID)
	except Class.DoesNotExist:
		raise Http404
	d = buildDict(Student.objects.get(user = request.user.id))
	d['theClass'] = theClass
	d['theLessons'] = Lesson.objects.filter(classes = theClass).order_by('date')
	return render(request, 'student/class.html', d)

@login_required
def allClasses(request):
	try:
		theStudent = Student.objects.get(user = request.user.id)
	except Student.DoesNotExist:
		raise Http404
	myClasses = theStudent.classes.all()
	return render(request, 'student/allClasses.html', {'theStudent':theStudent, 'myClasses':myClasses})

def startPage(request):
	if request.user.is_authenticated():
		if request.user.groups.filter(name = 'Admin').count():
			logout(request)
			return login(request)
		if request.user.groups.filter(name = 'Teacher').count():
			return teacher2Home(request, request.user)
		return studentHome(request)
	return login(request)

@login_required
def teacher2Home(request, teacherUser):
	theTeacher = Teacher.objects.get(user = teacherUser.id)
	return redirect('/teacher', {'theTeacher':theTeacher})

def logout(request):
	django.contrib.auth.logout(request)
	return startPage(request)

def login(request):
	if request.method == 'GET':
		form = LoginForm()
		return render_to_response('auth/login.html', {'form':form},
								  context_instance = RequestContext(request))

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			return render_to_response('auth/login.html', {'form':form},
								  context_instance = RequestContext(request))

		user = authenticate(username = request.POST['username'],
							password = request.POST['password'])
		if user is None:
			return render_to_response('auth/login.html',
									  {'form':form,
									   'error': 'Invalid username or password'},
									  context_instance = RequestContext(request))
		django.contrib.auth.login(request, user)
		if user.groups.filter(name = 'Teacher').count():
			return teacher2Home(request, user)
		return student2Home(request, user)

@login_required
def studentHome(request):
	try:
		theStudent = Student.objects.get(user = request.user.id)
	except Student.DoesNotExist:
		return redirect('/', {})
	myClasses = theStudent.classes.all()
	return render(request, 'student/studentHome.html', {'theStudent':theStudent, 'myClasses':myClasses})

@login_required
def student2Home(request, studentUser):
	theStudent = Student.objects.get(user = studentUser.id)
	return redirect('/student', {'theStudent':theStudent})
