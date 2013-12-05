# -*- coding: utf-8 -*-
from django.forms.widgets import Select, TextInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.util import flatatt
from django.utils.html import format_html
from django.template.loader import render_to_string


class ChainedSelectWidget(Select):
    def __init__(self, parent_name, url, *args, **kwargs):
        self.settings = {
            'data-parent-id': 'id_%s' % parent_name,
            'data-url': url
            }
        super(ChainedSelectWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        attrs = dict(self.settings, **{'class': 'chained','id': 'id_%s' % name })
        output = super(ChainedSelectWidget, self).render(name, value, attrs, choices)
        return mark_safe(output)





class ChainedTextWidget(Select):
    def __init__(self, parent_name, url, attrs=None, choices=()):
        self.display_settings = {
            'data-parent-id': 'id_%s' % parent_name,
            'data-url': url
            }

        self.settings = {
            'data-parent-id': 'id_%s' % parent_name,
            'data-url': url
            }

        self.choices = list(choices)
        super(Select, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''


        display_value = ''
        for k, v in self.choices:
            if k == value:
                display_value = v

        display_attrs = dict(self.display_settings, **{
            'id': 'id_%s_display' % name,
            'data-hidden-id': 'id_%s' % name,
            'class': 'chained',
            'value': display_value,
        })
        attrs = dict(self.settings, **{
            'id':'id_%s' % name,
            'name': name,
            'value': value,
            'class': 'chained'
        })


        return render_to_string('form/widgets/chained_text_widget.html', {
            'display_attrs': flatatt(display_attrs),
            'attrs': flatatt(attrs),
            'display_value': display_value
        })