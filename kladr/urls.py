# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^districts/(?P<region>\d+)/$', get_districts),
    url(r'^cities/(?P<district>\d+)/$', get_cities),
    url(r'^streets/(?P<city>\d+)/$', get_streets),
)
