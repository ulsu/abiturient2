from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^application/', include('form.urls')),
    url(r'^kladr/', include('kladr.urls')),
    url(r'^education/', include('education.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tiles/', include('tiles.urls')),
    url(r'^media/(?P<path>.*)$', mediaserver),
)
