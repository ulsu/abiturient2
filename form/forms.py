# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import RadioSelect
from django.forms.models import inlineformset_factory, modelformset_factory

from kladr.models import *
from kladr.forms import FormKLADRRelatesMixin

from models import Application, Exam
from widgets import ChainedSelectWidget, ChainedTextWidget

disabled = {'disabled': 'disabled'}

def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class DependentFormMixin(object):
    def _prepare_dependent_fields(self, fields, parent, parent_id, value=''):
        for f in fields:
            self.fields[f].widget.attrs.update({
                'data-dependent-field': parent_id,
                'data-dependent-value': str(value),
                'class': 'dependent'
            })
            value_is_forbidden = parent is None or\
                                 (value == '' and parent == '') or\
                                 (value != '' and parent.pk != value)
            if value_is_forbidden:
                self.fields[f].widget.attrs.update(disabled)

            # def field_clean_template():
            #     if value_is_forbidden:
            #         return None
            #
            # self.__setattr__('clean_%s' % f, field_clean_template)


    def field_cleaner(self, field_name, parent_field_name, model, parent_model):
        if field_name in self._errors:
            elem = model.objects.get(pk=self.data[field_name])
            parent = parent_model.objects.get(pk=self.data[parent_field_name])
            if elem and parent and elem.id.startswith(parent.id):
                self.cleaned_data[field_name] = elem
                del self._errors[field_name]


class FormRelatesMixin(object):
    def _prepare_form_relation(self, field, rel_field, parent_field, model):
        # Если родитель пустой, то детей не грузим и выключаем поле
        if not hasattr(self.instance, parent_field):
            self.fields[field].widget.attrs.update({'disabled': 'disabled'})
            self.fields[field].queryset=model.objects.none()
        else:
            parent = self.instance.__getattribute__(parent_field)
            # Иначе грузим детей только этого родителя
            self.fields[field].queryset=model.objects.filter(**{rel_field: parent})


class PersonalApplicationForm(ModelForm, DependentFormMixin):
    class Meta:
        model = Application
        widgets = {
            'IDSex': RadioSelect()
        }
        fields = ['LastName', 'FirstName', 'MiddleName', 'BirthDay', 'BirthPlace', 'IDSex',
                  'IDSocialStatus', 'Nationality', 'Citizenship', 'PassportSer',
                  'PassportNumb', 'CodUVD', 'PassportDate', 'PassportIssued']

    def __init__(self, *args, **kwargs):
        super(PersonalApplicationForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''

        citizenship_russia_data = {
            'parent': self.instance.Citizenship,
            'parent_id': 'id_Citizenship',
            'value': 1
        }
        citizenship_dependent_fields = [
            'PassportSer',
            'PassportNumb',
            'CodUVD',
            'PassportDate',
            'PassportIssued'
        ]
        self._prepare_dependent_fields(citizenship_dependent_fields, **citizenship_russia_data)



class ResidenceApplicationForm(ModelForm, DependentFormMixin, FormKLADRRelatesMixin):
    class Meta:
        model = Application

        fields = ['RegCountry', 'RegRegion', 'RegDistrict', 'RegCity', 'RegStreet', 'RegHouse',
                  'RegApartment', 'RegZipcode', 'ResEqualsReg',
                  'ResStreet', 'ResHouse', 'ResApartment', 'ResZipcode']

        widgets = {
            'RegDistrict': ChainedSelectWidget(
                parent_name='RegRegion',
                url='/kladr/districts/',
            ),

            'RegCity': ChainedTextWidget(
                parent_name='RegDistrict',
                url='/kladr/cities/',
            ),

            'RegStreet': ChainedTextWidget(
                parent_name='RegCity',
                url='/kladr/streets/',
            ),

            'ResStreet': ChainedTextWidget(
                url='/kladr/streets/01000001000/',
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ResidenceApplicationForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''

        # КЛАДРовые связи регионов, районов, городов и улиц
        self._prepare_KLADR_form_relation('RegDistrict', self.instance.RegRegion, District)
        self._prepare_KLADR_form_relation('RegCity', self.instance.RegDistrict, City)
        self._prepare_KLADR_form_relation('RegStreet', self.instance.RegCity, Street)

        # Улицы только города Ульяновска
        # TODO: Вынести id Ульяновска в КЛАДРе в настройки
        self.fields['ResStreet'].queryset=Street.objects.filter(id__startswith='01000001000')

        # Показывать регионы только если выбрана Россия
        self._prepare_dependent_fields(['RegRegion'], self.instance.RegCountry, 'id_RegCountry', 1)

        # Дом, квартира и индекс активируются только если выбран город
        city_non_empty_data = {'parent': self.instance.RegCity, 'parent_id': 'id_RegCity'}
        city_non_empty_fields = ['RegHouse', 'RegApartment', 'RegZipcode']
        self._prepare_dependent_fields(city_non_empty_fields, **city_non_empty_data)

    def clean(self):
        super(ResidenceApplicationForm, self).clean()
        self.field_cleaner('RegDistrict', 'RegRegion', District, Region)
        self.field_cleaner('RegCity', 'RegDistrict', City, District)
        self.field_cleaner('RegStreet', 'RegCity', Street, City)

        if 'ResEqualsReg' in self.data:
            self.cleaned_data['ResStreet'] = None
            self.cleaned_data['ResHouse'] = None
            self.cleaned_data['ResApartment'] = None
            self.cleaned_data['ResZipcode'] = None
        return self.cleaned_data

class ExamForm(ModelForm):
    class Meta:
        model = Exam
        exclude = ['application']

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].empty_label = ''

ExamFormSet = inlineformset_factory(Application, Exam, form=ExamForm, extra=1, max_num=5)