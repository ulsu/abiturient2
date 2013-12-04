# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import EducationItem, Application
from django.forms.models import inlineformset_factory
from django.forms.widgets import RadioSelect, HiddenInput, CheckboxSelectMultiple

class EducationForm(ModelForm):
    class Meta:
        model = EducationItem
        exclude = ['application']
        widgets = {
            'order': HiddenInput,
            'education_form': CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)


EducationFormSet = inlineformset_factory(Application, EducationItem, form=EducationForm, extra=1)