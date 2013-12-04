# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from forms import *
from education.forms import EducationFormSet


def get_forms(instance, POST):
    return {
        'personal_form': PersonalApplicationForm(POST, instance=instance),
        'residence_form': ResidenceApplicationForm(POST, instance=instance)
    }


def get_formsets(instance, POST):
    return {
        'exam_formset': ExamFormSet(POST, instance=instance),
        'edu_formset': EducationFormSet(POST, instance=instance)
    }

def forms_are_valid(forms):
    for f in forms:
        if not forms[f].is_valid:
            return False
    return True

def display_form(request, id=None, instance=None, POST=None):
    args = []
    kwargs = {}
    if instance is not None:
        kwargs['instance'] = instance

    if POST is not None:
        args.append(POST)

    context = {}
    if id is not None:
        context.update({'id': id})

    context.update(get_forms(instance, POST))
    context.update(get_formsets(instance, POST))

    t = loader.get_template('form/main.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))


def add_new(request):
    return display_form(request)



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
    instance = Application.objects.get(pk=id)
    return display_form(request, id=id, instance=instance)


def app_list(request):
    applications = Application.objects.all()
    t = loader.get_template('form/list.html')
    c = RequestContext(request, {'applications': applications})
    return HttpResponse(t.render(c))