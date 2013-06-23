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

def studentPassChange(request,usern):
    theTeacher = Teacher.objects.get(user=request.user.id)
    try:
        u = User.objects.get(username=usern)
        s = Student.objects.get(user=u.id)
    except Student.DoesNotExist:
        raise Http404
    
    if request.POST:
        form = StudentChangePasswordForm(request.POST)
        if form.is_valid():
            u.set_password(request.POST['password'])
            u.save()
            return studentInfo(request,usern)
    else:
        form = StudentChangePasswordForm()
    return render_to_response("teacher/changePassword.html", {
        "form": form,'s':s
    }, context_instance=RequestContext(request))
    
def studentInfoChange(request,usern):
    theTeacher = Teacher.objects.get(user=request.user.id)
    try:
        u = User.objects.get(username=usern)
        s = Student.objects.get(user=u.id)
    except Student.DoesNotExist:
        raise Http404
    
    if request.POST:
        form = StudentForm(request.POST, instance = s)
        if form.is_valid():
            form.save()
            return studentInfo(request,usern)
    else:
        form = StudentForm(instance = s)
    return render_to_response("teacher/changeInfo.html", {
        "form": form,'s':s
    }, context_instance=RequestContext(request))

def studentInfo(request,usern):
	s = Student.objects.get(user=User.objects.get(username=usern).id)
	theTeacher = Teacher.objects.get(user=request.user.id)
	return render(request, 'teacher/student.html', {'theTeacher':theTeacher, 's':s})

def allStudents(request):
	theStudents = Student.objects.all()
	theTeacher = Teacher.objects.get(user=request.user.id)
	return render(request,'teacher/allStudents.html', {'theTeacher':theTeacher, 'theStudents':theStudents})

@login_required
def addStudent(request):
    theTeacher = Teacher.objects.get(user=request.user.id)
    if request.method == 'GET':
        form = UserForm()
        return render_to_response('teacher/addStudent.html', {'form':form,'theTeacher':theTeacher,'create':True},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = UserForm(request.POST)
        if not form.is_valid():
            return render_to_response('teacher/addStudent.html', {'form':form,'theTeacher':theTeacher,'create':True},
                                  context_instance=RequestContext(request))

        try:
            u = User.objects.get(username=request.POST['username'])
            return render_to_response('teacher/addStudent.html',
                                      {'form':form,'theTeacher':theTeacher,
                                       'error':'Username already taken','create':True},
                                  context_instance=RequestContext(request))
        except User.DoesNotExist:
            pass

        if request.POST['password'] != request.POST['confirm']:
            return render_to_response('teacher/addStudent.html',
                                      {'form':form,'theTeacher':theTeacher,
                                       'error':'Passwords must match','create':True},
                                  context_instance=RequestContext(request))

        userO = User.objects.create_user(request.POST['username'],
                                        request.POST['email'],
                                        request.POST['password'])
        userO.save()
        person = Student.objects.create(user=userO,first_name=request.POST['first_name'],
                                            last_name=request.POST['last_name'],
                                            email=request.POST['email'])

        
        return teacherHome(request)

@login_required
def teacherHome(request):
	theTeacher = Teacher.objects.get(user=request.user.id)
	return render(request,'teacher/teacherHome.html',{'theTeacher':theTeacher})



