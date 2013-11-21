# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
                       url(r'^(?P<action>[\w\-]+)/(?P<value>\d+)/(?P<parent>\d+)/$', kladr),
                       )
