# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.http import HttpResponse
from django.utils import simplejson
from django.http import Http404
from django.shortcuts import get_object_or_404
from models import *

def generate_json(request, items):
    json = simplejson.dumps(items)
    return HttpResponse(json, mimetype='application/json')


def queryset2list(queryset):
    results = list(queryset)
    final = []
    for item in results:
        final.append({'value': item.pk, 'display': unicode(item)})
    return final


def queryset2json(request, queryset):
    results = list(queryset)
    final = []
    for item in results:
        final.append({'value': item.pk, 'display': unicode(item)})
    json = simplejson.dumps(final)
    return HttpResponse(json, mimetype='application/json')


def get_districts(request, region):
    districts = District.objects.filter(id__startswith=region)
    districts = queryset2list(districts)
    return generate_json(request, districts)


def get_cities(request, district):
    if 'term' in request.GET:
        term = request.GET['term']
    else:
        return generate_json(request, [])
    cities = City.objects.filter(id__startswith=district, name__istartswith=term)
    cities = queryset2list(cities)
    return generate_json(request, cities)


def get_streets(request, city):
    if 'term' in request.GET:
        term = request.GET['term']
    else:
        return generate_json(request, [])
    streets = Street.objects.filter(id__startswith=city, name__istartswith=term)
    streets = queryset2list(streets)
    return generate_json(request, streets)
