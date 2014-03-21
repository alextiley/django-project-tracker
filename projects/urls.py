from django.conf.urls import patterns, url
from projects import views

urlpatterns = patterns('',
	url(r'^$', views.read, name='read'),
	url(r'^create$', views.create, name='create'),
	url(r'^update/(?P<project_id>\d+)$', views.update, name='update'),
	url(r'^delete/(?P<project_id>\d+)$', views.delete, name='delete'),
	#url(r'^$', ProjectListView.as_view()),
)