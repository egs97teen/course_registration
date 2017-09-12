# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re
import datetime
import dateutil.relativedelta
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, userData):
		messages = []

		for field in userData:
			if len(userData[field]) == 0:
				fields = {
					'first_name':'First name',
					'last_name':'Last name',
					'email':'Email',
					'password':'Password',
					'confirm_pw':'Confirmation password',
					'birthday':'Birthday'
				}
				messages.append(fields[field]+' must be filled in')

		if len(userData['first_name']) < 2:
			messages.append('First name must be at least two characters long')

		if len(userData['last_name']) < 2:
			messages.append('Last name must be at least two characters long')

		if userData['first_name'].isalpha()==False or userData['last_name'].isalpha()==False:
			messages.append('Name must only contain letters')

		elif len(userData['last_name']) < 2:
			messages.apppend('Last name must be at least two characters long')

		if not EMAIL_REGEX.match(userData['email']):
			messages.append('Must enter a valid email')

		try:
			User.objects.get(email=userData['email'])
			messages.append('Email already registered')
		except:
			pass

		if len(userData['password']) < 8:
			messages.append('Password must be at least eight characters long')

		# if re.search('[0-9]', userData['password']) is None:
		# 	messages.append('Password must contain at least one number')
        #
		# if re.search('[A-Z]', userData['password']) is None:
		# 	messages.append('Password must contain at least one capital letter')

		if userData['password'] != userData['confirm_pw']:
			messages.append('Password and confirmation password must match')

		if userData['birthday']:
			birthday = datetime.datetime.strptime(userData['birthday'], '%Y-%m-%d')
			now = datetime.datetime.now()
			age = dateutil.relativedelta.relativedelta(now, birthday)

			if birthday > now:
				messages.append('Pick a date in the past')
			if age.years < 18:
				messages.append('Must be at least 18 years old to register')

		if len(messages) > 0:
			return messages
		else:
			hashed_pw=bcrypt.hashpw(userData['password'].encode(), bcrypt.gensalt())
			new_user= User.objects.create(first_name=userData['first_name'], last_name=userData['last_name'], email=userData['email'], hashed_pw=hashed_pw, birthday=userData['birthday'])
			return new_user.id

	def login(self, userData):
		messages = []
		for field in userData:
			if len(userData[field]) == 0:
				fields = {
					'login_email':'Email',
					'login_password':'Password'
				}
				messages.append(fields[field]+' must be filled in')

		try:
			user = User.objects.get(email=userData['login_email'])
			encrypted_pw = bcrypt.hashpw(userData['login_password'].encode(), user.hashed_pw.encode())
			if encrypted_pw==user.hashed_pw.encode():
				print ('Test worked')
				return user.id
			else:
				messages.append('Wrong password')
		except:
			messages.append('User not registered')

		if len(messages) > 0:
			return messages

class User(models.Model):
	first_name = models.CharField(max_length=250)
	last_name = models.CharField(max_length=250)
	email = models.CharField(max_length=250)
	hashed_pw = models.CharField(max_length=250)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects=UserManager()

class CourseManager(models.Manager):
    def add_new(self, data, user_id):
        messages = []

        for field in data:
            if len(data[field]) == 0:
                fields = {
                    'name': 'Course Name',
                    'date': 'Date',
                    'time': 'Time'
                    }
                messages.append(fields[field]+' must be filled in')

        if data['date']:
            # course_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
            # course_time = datetime.datetime.strptime(data['time'], '%H:%M')
            # today = datetime.datetime.today()

            course_dt = data['date'] + ' ' + data['time']
            course_dt = datetime.datetime.strptime(course_dt, "%Y-%m-%d %H:%M")
            #strptime takes a string representation or date and/or time as first arg and format string as second and returns a datetime object
            #strftime takes a datetime object as first arg and format string as second and returns a string
            now = datetime.datetime.now()

            if course_dt <= now:
                messages.append('Pick a date and time in the future')

        try:
            course = Course.objects.get(name=data['name'], time=data['time'], date = data['date'])
            messages.append("Course already offered at that time")
        except:
            user = User.objects.get(id=user_id)
            user_courses = Course.objects.filter(students__id=user.id) | Course.objects.filter(instructor__id=user.id)

            for course in user_courses:
                course_date = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
                course_time = datetime.datetime.strptime(data['time'], "%H:%M").time()

                if course_date == course.date and course_time == course.time:
                    messages.append("You're in a conflicting course")
                    break

        if len(messages) == 0:
            user = User.objects.get(id=user_id)
            new_course = Course.objects.create(name=data['name'], instructor=user, date=data['date'], time=data['time'])
            return new_course.id
        else:
            return messages


class Course(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey(User)
    students = models.ManyToManyField(User, related_name='courses_enrolled')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=CourseManager()
