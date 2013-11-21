# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.http import HttpResponse
from django.utils import simplejson
from django.http import Http404
from django.shortcuts import get_object_or_404
from models import *


def kladr(request, action, value, parent):
    if action == 'districts':
        qs = get_districts(value)
    elif action == 'cities':
        qs = get_cities(value, parent)
    else:
        raise Http404
    results = list(qs)
    final = []
    for item in results:
        final.append({'value': item.pk, 'display': unicode(item)})
    json = simplejson.dumps(final)
    return HttpResponse(json, mimetype='application/json')

def get_districts(value):
    region = get_object_or_404(Region, pk=value)
    return region.districts.all()

def get_cities(value, parent):
    if value == '0':
        region = get_object_or_404(Region, pk=parent)
        return City.objects.filter(region=region, district=None)
    else:
        district = get_object_or_404(District, pk=value)
        return district.cities.all()