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

def teacherHome(request):
	theTeacher = Teacher.objects.get(user=request.user.id)
	return render(request,'teacher/teacherHome.html',{'theTeacher':theTeacher})

