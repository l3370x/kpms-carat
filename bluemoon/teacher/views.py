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
from course.models import *
from lesson.models import *


def buildDict(theTeacher):
    d = {}
    d['theTeacher'] = theTeacher
    d['theClasses'] = Class.objects.all()
    return d

@login_required
def removeClass(request, classID):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    try:
        c = Class.objects.get(id = classID)
    except Class.DoesNotExist:
        raise Http404

    d['theClass'] = c
    d['message'] = "Do you want to delete this class?"
    d['prevLink'] = "/teacher"
    d['actionLink'] = "/teacher/class/" + classID + "/confirmedDelete/"
    return render(request, 'teacher/confirmDeleteClass.html', d)

@login_required
def removeClassConfirmed(request, classID):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    try:
        c = Class.objects.get(id = classID)
    except:
        raise Http404

    c.delete()
    return teacherHome(request)

@login_required
def lessonInfo(request, lessonID):
    try:
        l = Lesson.objects.get(id = lessonID)
    except Lesson.DoesNotExist:
        raise Http404

    if request.POST:
        form = LessonForm(request.POST, instance = l)
        if form.is_valid():
            form.save()
    else:
        form = LessonForm(instance = l)
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    d['l'] = l
    d['form'] = form
    return render(request, 'teacher/lesson.html', d)

@login_required
def addLessonToClass(request, classID):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    d['classID'] = classID
    try:
        c = Class.objects.get(id = classID)
        d['theClass'] = c
    except Class.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        form = LessonForm()
        d['form'] = form
        return render_to_response('teacher/addLesson.html', d,
                                  context_instance = RequestContext(request))

    if request.method == 'POST':
        form = LessonForm(request.POST)
        d['form'] = form
        if not form.is_valid():
            return render_to_response('teacher/addLesson.html', d,
                                  context_instance = RequestContext(request))


        classO = form.save()
        classO.save()
        classO.classes.add(c)
        classO.save()
        return teacherHome(request)

@login_required
def addStudentsToClass(request, classID):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    try:
        c = Class.objects.get(id = classID)
        d['c'] = c
    except Class.DoesNotExist:
        raise Http404
    theStudents = Student.objects.filter().order_by('last_name')
    d['theStudents'] = theStudents
    return render(request, 'teacher/addStudentToClass.html', d)


@login_required
def classTitleChange(request, classID):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    d['classID'] = classID
    try:
        c = Class.objects.get(id = classID)
        d['c'] = c
    except Class.DoesNotExist:
        raise Http404

    if request.POST:
        form = ClassTitleForm(request.POST, instance = c)
        d['form'] = form
        if form.is_valid():
            form.save()
            return classInfo(request, classID)
    else:
        form = ClassTitleForm(instance = c)
        d['form'] = form
    return render_to_response("teacher/changeClassTitle.html", d, context_instance = RequestContext(request))

@login_required
def classInfo(request, classID):
    try:
        c = Class.objects.get(id = classID)
    except Class.DoesNotExist:
        raise Http404

    if request.POST:
        form = ClassNotesForm(request.POST, instance = c)
        if form.is_valid():
            form.save()
    else:
        form = ClassNotesForm(instance = c)
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    d['form'] = form
    theLessons = Lesson.objects.filter(classes = c.id)
    d['theLessons'] = theLessons
    theStudents = Student.objects.filter(classes = c.id)
    d['theStudents'] = theStudents
    d['c'] = c
    return render(request, 'teacher/class.html', d)

@login_required
def allClasses(request):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    return render(request, 'teacher/allClasses.html', d)

@login_required
def addClass(request):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    if request.method == 'GET':
        form = ClassForm()
        d['form'] = form
        return render_to_response('teacher/addClass.html', d,
                                  context_instance = RequestContext(request))

    if request.method == 'POST':
        form = ClassForm(request.POST)
        d['form'] = form
        if not form.is_valid():
            return render_to_response('teacher/addClass.html', d,
                                  context_instance = RequestContext(request))


        classO = form.save()
        classO.save()
        return teacherHome(request)

@login_required
def studentPassChange(request, usern):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    try:
        u = User.objects.get(username = usern)
        s = Student.objects.get(user = u.id)
    except Student.DoesNotExist:
        raise Http404
    d['s'] = s
    if request.POST:
        form = StudentChangePasswordForm(request.POST)
        d['form'] = form
        if form.is_valid():
            u.set_password(request.POST['password'])
            u.save()
            return studentInfo(request, usern)
    else:
        form = StudentChangePasswordForm()
        d['form'] = form
    return render_to_response("teacher/changePassword.html", d, context_instance = RequestContext(request))

@login_required
def studentInfoChange(request, usern):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    try:
        u = User.objects.get(username = usern)
        s = Student.objects.get(user = u.id)
    except Student.DoesNotExist:
        raise Http404
    d['s'] = s
    if request.POST:
        form = StudentForm(request.POST, instance = s)
        d['form'] = form
        if form.is_valid():
            form.save()
            return studentInfo(request, usern)
    else:
        form = StudentForm(instance = s)
        d['form'] = form
    return render_to_response("teacher/changeInfo.html", d, context_instance = RequestContext(request))

@login_required
def studentInfo(request, usern):
    s = Student.objects.get(user = User.objects.get(username = usern).id)
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    d['s'] = s
    return render(request, 'teacher/student.html', d)

@login_required
def allStudents(request):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    d['theStudents'] = Student.objects.all()
    return render(request, 'teacher/allStudents.html', d)

@login_required
def addStudent(request):
    theTeacher = Teacher.objects.get(user = request.user.id)
    d = buildDict(theTeacher)
    if request.method == 'GET':
        form = UserForm()
        d['form'] = form
        return render_to_response('teacher/addStudent.html', d, context_instance = RequestContext(request))

    if request.method == 'POST':
        form = UserForm(request.POST)
        d['form'] = form
        if not form.is_valid():
            return render_to_response('teacher/addStudent.html', d, context_instance = RequestContext(request))

        try:
            u = User.objects.get(username = request.POST['username'])
            d['error'] = 'Username already taken'
            return render_to_response('teacher/addStudent.html', d, context_instance = RequestContext(request))
        except User.DoesNotExist:
            pass

        if request.POST['password'] != request.POST['confirm']:
            d['error'] = 'Passwords must match'
            return render_to_response('teacher/addStudent.html', d, context_instance = RequestContext(request))

        userO = User.objects.create_user(request.POST['username'],
                                        request.POST['email'],
                                        request.POST['password'])
        userO.save()
        person = Student.objects.create(user = userO, first_name = request.POST['first_name'],
                                            last_name = request.POST['last_name'],
                                            email = request.POST['email'])


        return allStudents(request)

@login_required
def teacherHome(request):
    try:
        theTeacher = Teacher.objects.get(user = request.user.id)
    except Teacher.DoesNotExist:
        return redirect('/', {})
    d = buildDict(theTeacher)
    return render(request, 'teacher/teacherHome.html', d)



