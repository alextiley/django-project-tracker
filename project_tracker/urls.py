from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='projects/', permanent=True)),
   	url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^admin/', include(admin.site.urls))
)