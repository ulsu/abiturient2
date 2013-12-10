# -*- coding: utf-8 -*-
from django.views.static import serve
from django.conf import settings

def mediaserver(request, path):
    return serve(request, path, settings.MEDIA_ROOT)
