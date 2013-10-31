# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Application, Exam
from django.forms.widgets import RadioSelect
from django.forms.models import inlineformset_factory, modelformset_factory
import datetime

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        widgets = {
            'IDSex': RadioSelect()
        }
        exclude = ['user', 'Edited']

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''


class ExamForm(ModelForm):
    class Meta:
        model = Exam
        exclude = ['application']

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''



ExamFormSet = inlineformset_factory(Application, Exam, form=ExamForm, extra=1)

