# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from forms import *


def get_forms(instance=None, POST=None):
    args = []
    kwargs = {}
    if instance is not None:
        kwargs['instance'] = instance

    if POST is not None:
        args.append(POST)


    return {
        'personal_form': PersonalApplicationForm(*args, **kwargs),
        'residence_form': ResidenceApplicationForm(*args, **kwargs)
    }

def forms_are_valid(forms):
    is_valid = True
    for f in forms:
        if not forms[f].is_valid:
            is_valid = False
            return is_valid

    if is_valid:
        return is_valid


def add_new(request):
    forms = get_forms()
    exam_formset = ExamFormSet()
    t = loader.get_template('form/main.html')
    c = RequestContext(request, {'forms': forms, 'exam_formset': exam_formset})
    return HttpResponse(t.render(c))


def save(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            instance = Application.objects.get(pk=request.POST['id'])
        else:
            instance = Application.objects.create()

        forms = get_forms(instance=instance, POST=request.POST)
        if forms_are_valid(forms):
            for f in forms:
                forms[f].save()

        exam_formset = ExamFormSet(request.POST, instance=instance)
        if exam_formset.is_valid():
            exam_formset.save()


    applications = Application.objects.all()
    t = loader.get_template('form/list.html')
    c = RequestContext(request, {'applications': applications})
    return HttpResponse(t.render(c))


def edit(request, id):
    a = Application.objects.get(pk=id)
    forms = get_forms(instance=a)
    exam_formset = ExamFormSet(instance=a)
    t = loader.get_template('form/main.html')
    c = RequestContext(request, {'forms': forms, 'id': id, 'exam_formset': exam_formset})
    return HttpResponse(t.render(c))


def app_list(request):
    applications = Application.objects.all()
    t = loader.get_template('form/list.html')
    c = RequestContext(request, {'applications': applications})
    return HttpResponse(t.render(c))