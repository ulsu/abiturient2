# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from models import *
from forms import *
from education.forms import EducationFormSet


def get_forms(kwargs):
    return {
        'personal_form': PersonalApplicationForm(**kwargs),
        'residence_form': ResidenceApplicationForm(**kwargs),
        'certificate_form': CertificateForm(**kwargs),
    }


def get_formsets(kwargs):
    return {
        'exam_formset': ExamFormSet(**kwargs),
        'edu_formset': EducationFormSet(**kwargs),
    }


def are_valid(forms):
    for f in forms:
        if not forms[f].is_valid():
            return False
    return True


def app_list(request):
    applications = Application.objects.all()
    t = loader.get_template('form/list.html')
    c = RequestContext(request, {'applications': applications})
    return HttpResponse(t.render(c))


def render_form(request, context):
    t = loader.get_template('form/main.html')
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))


def get_instance_and_url(request, id):
    if id is None:
        return Application.objects.create()
    else:
        return get_object_or_404(Application, pk=id)


def form(request, id=None):
    instance = get_instance_and_url(request, id)
    url = request.path
    context = {'id': id, 'url': url}
    if request.method == 'POST':
        kwargs = {'instance': instance, 'data': request.POST}
        forms = get_forms(kwargs)
        formsets = get_formsets(kwargs)

        if are_valid(forms) and are_valid(formsets):
            for f in forms:
                forms[f].save()
            for f in formsets:
                formsets[f].save()
            return redirect(url)
        else:
            context.update(forms)
            context.update(formsets)
            return render_form(request, context)
    else:
        kwargs = {'instance': instance}
        context.update(get_forms(kwargs))
        context.update(get_formsets(kwargs))
        return render_form(request, context)

