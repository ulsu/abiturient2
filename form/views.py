# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from forms import ApplicationForm, ExamFormSet


def add_new(request):
    form = ApplicationForm()
    exam_formset = ExamFormSet()
    t = loader.get_template('form/main.html')
    c = RequestContext(request, {'form': form, 'exam_formset': exam_formset})
    return HttpResponse(t.render(c))


def save(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            instance = Application.objects.get(pk=request.POST['id'])
            a = ApplicationForm(request.POST, instance=instance)
        else:
            a = ApplicationForm(request.POST)
        app = a.save()

        exam_formset = ExamFormSet(request.POST, instance=app)
        if exam_formset.is_valid():
            exam_formset.save()


    applications = Application.objects.all()
    t = loader.get_template('form/list.html')
    c = RequestContext(request, {'applications': applications})
    return HttpResponse(t.render(c))


def edit(request, id):
    a = Application.objects.get(pk=id)
    form = ApplicationForm(instance=a)
    exam_formset = ExamFormSet(instance=a)
    t = loader.get_template('form/main.html')
    c = RequestContext(request, {'form': form, 'id': id, 'exam_formset': exam_formset})
    return HttpResponse(t.render(c))


def app_list(request):
    applications = Application.objects.all()
    t = loader.get_template('form/list.html')
    c = RequestContext(request, {'applications': applications})
    return HttpResponse(t.render(c))