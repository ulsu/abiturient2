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

class SelectWidget(Select):
    def render(self, name, value, attrs=None, choices=()):
        self.name = name
        output = super(SelectWidget, self).render(name, value, attrs, choices)
        return mark_safe(output)


class ChainedTextWidget(Select):
    def __init__(self, url, parent_name=None, attrs=None, choices=()):
        settings = {
            'data-url': url
        }

        if parent_name is not None:
            settings['data-parent-id'] = 'id_%s' % parent_name

        self.display_settings = settings
        self.hidden_settings = settings

        self.choices = list(choices)
        self.attrs = attrs
        super(Select, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        if self.attrs is None:
            attrs = {}
        else:
            attrs = self.attrs

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

        hidden_attrs = dict(self.hidden_settings, **{
            'id':'id_%s' % name,
            'name': name,
            'value': value,
            'class': 'chained'
        })

        display_attrs.update(attrs)

        return render_to_string('form/widgets/chained_text_widget.html', {
            'display_attrs': flatatt(display_attrs),
            'attrs': flatatt(hidden_attrs),
            'display_value': display_value
        })
