# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import RadioSelect, HiddenInput, CheckboxSelectMultiple, Select

from form.widgets import *
from form.forms import FormRelatesMixin

from models import EducationItem, Faculty, Application, Speciality


class EducationForm(ModelForm, FormRelatesMixin):
    class Meta:
        model = EducationItem
        exclude = ['application']

        widgets = {
            'order': HiddenInput,
            'education_form': CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if hasattr(self.fields[f], 'empty_label') and self.fields[f].empty_label:
                self.fields[f].empty_label = ''
        self.fields['faculty'].widget = ChainedSelectWidget(
            parent_name=self.add_prefix('direction'),
            url='/education/faculties/',
            )

        self._prepare_form_relation('faculty', 'speciality__direction', 'direction', Faculty)





EducationFormSet = inlineformset_factory(Application, EducationItem, form=EducationForm, extra=1)