# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Course
from django.db.models import Q
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	if 'user' in request.session:   
		return render(request, 'course_app/courses.html')
	else:
		return render(request, 'course_app/index.html')

def login(request):
	if request.method=='POST': # used to prevent user from directly accessing this page (ex: localhost:8000/login)
		login = User.objects.login(request.POST.copy()) # access method, "login," in model
		if isinstance(login, list):
			for item in login:
				messages.error(request, item)
			return redirect('/')
		else:
			request.session['user'] = login
			messages.success(request, 'Successfully logged in!')
			return redirect(reverse('courses'))
	else:
		return redirect('/')

def register(request):
	if request.method=='POST':
		register = User.objects.register(request.POST.copy())
		if isinstance(register, list):
			for item in register:
				messages.error(request, item)
			return redirect('/')
		else:
			request.session['user'] = register
			messages.success(request, 'Successfully registered!')
			return redirect(reverse('courses'))
	else:
		return redirect('/')

def courses(request):
    if 'user' in request.session:
        user = User.objects.get(id=request.session['user']) # Get entire object of current user
        courses = Course.objects.filter(Q(students__id=user.id) | Q(instructor__id=user.id)).order_by('date')
        # filters whether current user is a student in a course OR an instructor of a course
        # Q is used to merge both filters in one query
        # Must use the same model
        context = {
			'name':user.first_name+' '+user.last_name,
            'courses': courses
		}
        return render(request, 'course_app/courses.html', context)
    else:
        messages.error(request, 'Log in or register first')
        return redirect('/')

def course(request, course_id):
    course = Course.objects.get(id=course_id) # Get course with id of passed course_id
    students = User.objects.filter(courses_enrolled=course) # Of all users, find all students enrolled in course we got
    context = {
        'course': course,
        'students': students
    }
    return render(request, 'course_app/course.html', context)

def add_class(request, course_id):
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user'])
    add_course = course.students.add(user) # add course with id of passed course_id to current user
    return redirect(reverse('course', kwargs={'course_id':course.id}))

def drop_class(request, course_id):
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user'])
    drop_course = course.students.remove(user) # drop course with id of passed course_id from current user
    return redirect(reverse('courses'))

def delete_class(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete() # delete course with id of passed course_id
    return redirect(reverse('courses'))

def new(request): # when they click Create Course, take them to create new course page
    return render(request, 'course_app/new.html')

def add_new(request):
    post_data = request.POST.copy()
    result = Course.objects.add_new(post_data, request.session['user'])
    if isinstance(result, list):
        for err in result:
            messages.error(request, err)
        return redirect(reverse('new'))
    else:
        return redirect(reverse('courses'))

def enroll(request):
    other_courses = Course.objects.exclude(students__id=request.session['user']).exclude(instructor__id=request.session['user'])
    # All other courses available by excluding courses where current user is a student or instructor
    context = {
        'courses': other_courses
    }
    return render(request, 'course_app/enroll.html', context)

def logout(request):
	request.session.pop('user')
	return redirect('/')
