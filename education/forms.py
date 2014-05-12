# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import RadioSelect, HiddenInput, CheckboxSelectMultiple, Select, TextInput, DateInput

from form.widgets import *
from form.forms import FormRelatesMixin

from models import *


class EducationItemForm(ModelForm, FormRelatesMixin):
    class Meta:
        model = EducationItem
        exclude = ['application']

        widgets = {
            'order': HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(EducationItemForm, self).__init__(*args, **kwargs)
        #
        # if self.instance:
        #     self._prepare_form_relation('faculty', 'direction', 'direction', Speciality)
        #     self._prepare_form_relation('education_form', 'speciality', 'faculty', SpecialityItem)
        # else:
        #     self.fields['faculty'].queryset=Speciality.objects.all()
        #     self.fields['education_form'].queryset=SpecialityItem.objects.all()
        #
        self.fields['faculty'].widget = ChainedSelectWidget(
            parent_name=self.add_prefix('direction'),
            url='/education/faculties/'
        )
        self.fields['education_form'].widget = ChainedCheckboxSelectMultiple(
            parent_name=self.add_prefix('faculty'),
            url='/education/edu_forms/',
            item_prefix=self.add_prefix('education_form')
        )
        self.fields['education_form'].help_text = ''

        for f in self.fields:
            if hasattr(self.fields[f], 'empty_label') and self.fields[f].empty_label:
                self.fields[f].empty_label = ''
                if type(self.fields[f].widget) in (TextInput, Select, DateInput, SelectWidget, ChainedTextWidget, ChainedSelectWidget):
                    self.fields[f].widget.attrs.update({'class':'form-control'})

        self.fields['order'].widget.attrs.update({'data-formset-order': ''})

        if not kwargs.get('data'):
            self._prepare_form_relation('faculty', 'direction', 'direction', Speciality)
            self._prepare_form_relation('education_form', 'speciality', 'faculty', SpecialityItem)
        else:
            self.fields['faculty'].queryset=Speciality.objects.all()
            self.fields['education_form'].queryset=SpecialityItem.objects.all()

EducationFormSet = inlineformset_factory(Application, EducationItem, form=EducationItemForm, extra=1, max_num=3)


class EducationItemForm(ModelForm, FormRelatesMixin):
    class Meta:
        model = EducationItem
        exclude = ['application']

        widgets = {
            'order': HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(EducationItemForm, self).__init__(*args, **kwargs)
        #
        # if self.instance:
        #     self._prepare_form_relation('faculty', 'direction', 'direction', Speciality)
        #     self._prepare_form_relation('education_form', 'speciality', 'faculty', SpecialityItem)
        # else:
        #     self.fields['faculty'].queryset=Speciality.objects.all()
        #     self.fields['education_form'].queryset=SpecialityItem.objects.all()
        #
        self.fields['faculty'].widget = ChainedSelectWidget(
            parent_name=self.add_prefix('direction'),
            url='/education/faculties/'
        )
        self.fields['education_form'].widget = ChainedCheckboxSelectMultiple(
            parent_name=self.add_prefix('faculty'),
            url='/education/edu_forms/',
            item_prefix=self.add_prefix('education_form')
        )
        self.fields['education_form'].help_text = ''

        for f in self.fields:
            if hasattr(self.fields[f], 'empty_label') and self.fields[f].empty_label:
                self.fields[f].empty_label = ''
                if type(self.fields[f].widget) in (TextInput, Select, DateInput, SelectWidget, ChainedTextWidget, ChainedSelectWidget):
                    self.fields[f].widget.attrs.update({'class':'form-control'})

        self.fields['order'].widget.attrs.update({'data-formset-order': ''})

        if not kwargs.get('data'):
            self._prepare_form_relation('faculty', 'direction', 'direction', Speciality)
            self._prepare_form_relation('education_form', 'speciality', 'faculty', SpecialityItem)
        else:
            self.fields['faculty'].queryset=Speciality.objects.all()
            self.fields['education_form'].queryset=SpecialityItem.objects.all()

EducationFormSet = inlineformset_factory(Application, EducationItem, form=EducationItemForm, extra=1, max_num=3)