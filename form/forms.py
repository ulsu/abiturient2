# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Application, Exam
from kladr.models import *
from django.forms.widgets import RadioSelect
from django.forms.models import inlineformset_factory, modelformset_factory
import datetime
from kladr.widgets import KladrSelectWidget, KladrTextWidget

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
            'RegDistrict': KladrSelectWidget(
            parent_name='RegRegion',
            action='districts',
            accept_empty=False,
            empty_label='Нет',
            ),

            'RegCity': KladrTextWidget(
            parent_name='RegDistrict',
            grandparent_name='RegRegion',
            action='cities',
            accept_empty=True,
            empty_label='',
            ),

            'RegStreet': KladrTextWidget(
            parent_name='RegCity',
            action='streets',
            accept_empty=False,
            empty_label='',
            )
        }

    def __init__(self, *args, **kwargs):
        super(ResidenceApplicationForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''

        self.fields['RegDistrict'].queryset = District.objects.filter(region=self.initial['RegRegion'])
        self.fields['RegDistrict'].empty_label = 'Нет'

        self.fields['RegCity'].queryset = City.objects.filter(
            region=self.instance.RegRegion,
            district=self.instance.RegDistrict
        )

        self.fields['RegStreet'].queryset = Street.objects.filter(
            region=self.instance.RegRegion,
            district=self.instance.RegDistrict,
            city=self.instance.RegCity
        )

    def clean(self):
        super(ResidenceApplicationForm, self).clean()
        if 'RegDistrict' in self._errors:
            district = District.objects.get(pk=self.data['RegDistrict'])
            self.initial['RegDistrict'] = district.id
            self.cleaned_data['RegDistrict'] = district
            del self._errors['RegDistrict']

        if 'RegCity' in self._errors:
            city = City.objects.get(pk=self.data['RegCity'])
            self.initial['RegCity'] = city.id
            self.cleaned_data['RegCity'] = city
            del self._errors['RegCity']

        if 'RegStreet' in self._errors:
            city = Street.objects.get(pk=self.data['RegStreet'])
            self.initial['RegStreet'] = city.id
            self.cleaned_data['RegStreet'] = city
            del self._errors['RegStreet']

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