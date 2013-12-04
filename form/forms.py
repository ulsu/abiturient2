# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Application, Exam
from kladr.models import *
from django.forms.widgets import RadioSelect
from django.forms.models import inlineformset_factory, modelformset_factory
import datetime
from kladr.widgets import KladrSelectWidget, KladrTextWidget
from widgets import ChainedSelectWidget, ChainedTextWidget

class PersonalApplicationForm(ModelForm):
    class Meta:
        model = Application
        widgets = {
            'IDSex': RadioSelect()
        }
        fields = ['LastName', 'FirstName', 'MiddleName', 'BirthDay', 'IDSex',
                  'IDSocialStatus', 'Nationality', 'Citizenship', 'PassportSer',
                  'PassportNumb', 'CodUVD', 'PassportDate', 'BirthPlace', 'PassportIssued']

    def __init__(self, *args, **kwargs):
        super(PersonalApplicationForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''

class ResidenceApplicationForm(ModelForm):
    class Meta:
        model = Application

        fields = ['RegCountry', 'RegRegion', 'RegDistrict', 'RegCity', 'RegStreet', 'RegHouse',
                  'RegApartment', 'RegZipcode',
                  'ResStreet', 'ResHouse', 'ResApartment', 'ResZipcode']

        widgets = {
            'RegDistrict': ChainedSelectWidget(
                parent_name='RegRegion',
                url='/kladr/districts/'
            ),

            'RegCity': ChainedTextWidget(
                parent_name='RegDistrict',
                url='/kladr/cities/'
            ),

            # 'RegStreet': KladrTextWidget(
            # parent_name='RegCity',
            # action='streets',
            # accept_empty=False,
            # empty_label='',
            # ),

        }

    def __init__(self, *args, **kwargs):
        super(ResidenceApplicationForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''


        # self.fields['RegStreet'].queryset = Street.objects.filter(
        #     region=self.instance.RegRegion,
        #     district=self.instance.RegDistrict,
        #     city=self.instance.RegCity
        # )

    def clean(self):
        return self.cleaned_data

class ExamForm(ModelForm):
    class Meta:
        model = Exam
        exclude = ['application']


    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''

ExamFormSet = inlineformset_factory(Application, Exam, form=ExamForm, extra=1)