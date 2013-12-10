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


def get_faculties(request, direction):
    faculties = Faculty.objects.filter(speciality__direction__id=direction)
    faculties = queryset2list(faculties)
    return generate_json(request, faculties)