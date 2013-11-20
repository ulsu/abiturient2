from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^application/', include('form.urls')),
    url(r'^chained/', include('chained_selects.urls')),
    url(r'^kladr/', include('kladr.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
