from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'register$', views.register, name='register'),
  url(r'login$', views.login, name='login'),
  url(r'logout$', views.logout, name='logout'),
  url(r'courses$', views.courses, name='courses'),
  url(r'courses/new$', views.new, name='new'),
  url(r'add_new$', views.add_new, name='add_new'),
  url(r'courses/(?P<course_id>\d+)$', views.course, name='course'),
  url(r'enroll$', views.enroll, name='enroll'),
  url(r'add_class/(?P<course_id>\d+)$', views.add_class, name='add_class'),
  url(r'drop_class/(?P<course_id>\d+)$', views.drop_class, name='drop_class'),
  url(r'delete_class/(?P<course_id>\d+)$', views.delete_class, name='delete_class')
]
