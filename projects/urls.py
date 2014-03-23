from django.conf.urls import patterns, url

from .views import CreateView
from .views import ListView
from .views import UpdateView
from .views import DeleteView

urlpatterns = patterns('',
	url(r'^$', ListView.as_view(), name='list'),
	url(r'^create$', CreateView.as_view(), name='create'),
	url(r'^update/(?P<project_id>\d+)$', UpdateView.as_view(), name='update'),
	url(r'^delete/(?P<project_id>\d+)$', DeleteView.as_view(), name='delete'),
)