# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
                       url(r'^(?P<slug>\w+)/$', view),
                       url(r'^(?P<slug>\w+)/(?P<id>\d+)/$', show),
                       )