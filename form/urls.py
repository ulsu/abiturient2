from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^add/$', add_new),
    url(r'^save/$', save),
    url(r'^list/$', app_list),
    url(r'^edit/(?P<id>\d+)/$', edit),
)
