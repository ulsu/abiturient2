# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.forms.widgets import Select, CheckboxSelectMultiple, CheckboxInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.util import flatatt
from django.template.loader import render_to_string
from itertools import chain
from django.utils.html import format_html

class ChainedSelectWidget(Select):
    def __init__(self, parent_name, url, *args, **kwargs):
        self.settings = {
            'data-parent-id': 'id_%s' % parent_name,
            'data-url': url
            }
        super(ChainedSelectWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        classname = '%s %s' % (self.attrs['class'], 'chained') if 'class' in self.attrs else 'chained'
        attrs = dict(self.settings, **{'class': classname,'id': 'id_%s' % name })
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

        classname = '%s %s' % (self.attrs['class'], 'chained') if 'class' in self.attrs else 'chained'

        display_attrs = dict(self.display_settings, **{
            'id': 'id_%s_display' % name,
            'data-hidden-id': 'id_%s' % name,
            'class': classname,
            'value': display_value,
        })

        hidden_attrs = dict(self.hidden_settings, **{
            'id':'id_%s' % name,
            'name': name,
            'value': value,
            'class': 'chained'
        })

        return render_to_string('form/widgets/chained_text_widget.html', {
            'display_attrs': flatatt(display_attrs),
            'attrs': flatatt(hidden_attrs),
            'display_value': display_value
        })


class ChainedCheckboxSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, url, item_prefix, parent_name=None, *args, **kwargs):
        self.settings = {
            'data-parent-id': 'id_%s' % parent_name,
            'data-url': url,
            'class': 'chained',
            'data-item-prefix': item_prefix,
            'id': '%s_ul' % item_prefix
        }
        super(ChainedCheckboxSelectMultiple, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<ul %s>' % flatatt(self.settings)]
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html('<li><label{0}>{1} {2}</label></li>',
                                      label_for, rendered_cb, option_label))
        output.append('</ul>')
        return mark_safe('\n'.join(output))