from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^add/$', form),
    url(r'^edit/(?P<id>\d+)/$', form),
    url(r'^list/$', app_list),
)
