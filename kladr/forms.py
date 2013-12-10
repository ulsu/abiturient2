# -*- coding: utf-8 -*-

class FormKLADRRelatesMixin(object):
    def _prepare_KLADR_form_relation(self, field, parent, model):
        # Если родитель пустой, то детей не грузим и выключаем поле
        if parent is None:
            self.fields[field].widget.attrs.update({'disabled': 'disabled'})
            self.fields[field].queryset=model.objects.none()
        else:
            # Иначе грузим детей только этого родителя
            self.fields[field].queryset=model.objects.filter(id__startswith=parent.pk)