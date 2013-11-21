# -*- coding: utf-8 -*-
from django.forms.widgets import Select, TextInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.util import flatatt
from django.utils.html import format_html
from django.template.loader import render_to_string


class KladrSelectWidget(Select):
    def __init__(self, parent_name,  action, accept_empty, empty_label, grandparent_name='', *args, **kwargs):
        self.datas = {
            'data-parent-id': 'id_%s' % parent_name,
            'data-url': '/kladr/%s/' % action,
            'data-accept-empty': accept_empty,
            'data-empty-label': empty_label,
            'data-grandparent-id': grandparent_name
        }
        super(KladrSelectWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        attrs = dict(self.datas, **{'class': 'kladr', 'id': 'id_%s' % name })
        output = super(KladrSelectWidget, self).render(name, value, attrs, choices)
        return mark_safe(output)


class KladrTextWidget(Select):

    def __init__(self, parent_name,  action, accept_empty, empty_label, grandparent_name='', attrs=None, choices=()):
        self.datas = {
            'data-parent-id': 'id_%s' % parent_name,
            'data-url': '/kladr/%s/' % action,
            'data-accept-empty': accept_empty,
            'data-empty-label': empty_label,
            'data-grandparent-id': grandparent_name
        }

        self.choices = list(choices)
        super(Select, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        display_attrs = dict(self.datas, **{'class': 'kladr', 'id': 'id_%s_display' % name })
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            final_attrs['value'] = value
        return render_to_string('kladr/widgets/kladr_text_widget.html', {
            'display_attrs': flatatt(display_attrs),
            'final_attrs': flatatt(final_attrs),
            'choices': choices
        })
