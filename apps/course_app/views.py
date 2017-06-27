# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Course
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	if 'user' in request.session:
		return render(request, 'course_app/courses.html')
	else:
		return render(request, 'course_app/index.html')

def login(request):
	if request.method=='POST':
		login = User.objects.login(request.POST.copy())
		if isinstance(login, list):
			for item in login:
				messages.error(request, item)
			return redirect('/')
		else:
			request.session['user'] = login.id
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
			request.session['user'] = register.id
			messages.success(request, 'Successfully registered!')
			return redirect(reverse('courses'))
	else:
		return redirect('/')

def courses(request):
	if 'user' in request.session:
		user = User.objects.get(id=request.session['user'])
		context = {
			'name':user.first_name+' '+user.last_name
		}
		return render(request, 'course_app/courses.html', context)
	else:
		messages.error(request, 'Log in or register first')
		return redirect('/')

def logout(request):
	if request.method=='POST':
		request.session.pop('user')
		return redirect('/')
	else:
		return redirect('/')
