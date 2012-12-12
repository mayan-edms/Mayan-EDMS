import os
from itertools import chain

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms
from django.forms.util import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode


class PlainWidget(forms.widgets.Widget):
    """
    Class to define a form widget that effectively nulls the htmls of a
    widget and reduces the output to only it's value
    """
    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % value)


class DetailSelectMultiple(forms.widgets.SelectMultiple):
    def __init__(self, queryset=None, *args, **kwargs):
        self.queryset = queryset
        super(DetailSelectMultiple, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=(), *args, **kwargs):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        css_class = final_attrs.get('class', 'list')
        output = u'<ul class="%s">' % css_class
        options = None
        if value:
            if getattr(value, '__iter__', None):
                options = [(index, string) for index, string in \
                    self.choices if index in value]
            else:
                options = [(index, string) for index, string in \
                    self.choices if index == value]
        else:
            if self.choices:
                if self.choices[0] != (u'', u'---------') and value != []:
                    options = [(index, string) for index, string in \
                        self.choices]

        if options:
            for index, string in options:
                if self.queryset:
                    try:
                        output += u'<li><a href="%s">%s</a></li>' % (
                            self.queryset.get(pk=index).get_absolute_url(),
                            string)
                    except AttributeError:
                        output += u'<li>%s</li>' % (string)
                else:
                    output += u'<li>%s</li>' % string
        else:
            output += u'<li>%s</li>' % _(u"None")
        return mark_safe(output + u'</ul>\n')


def exists_with_famfam(path):
    try:
        return two_state_template(os.path.exists(path))
    except Exception, exc:
        return exc


def two_state_template(state, famfam_ok_icon=u'tick', famfam_fail_icon=u'cross'):
    if state:
        return mark_safe(u'<span class="famfam active famfam-%s"></span>' % famfam_ok_icon)
    else:
        return mark_safe(u'<span class="famfam active famfam-%s"></span>' % famfam_fail_icon)


class TextAreaDiv(forms.widgets.Widget):
    """
    Class to define a form widget that simulates the behavior of a
    Textarea widget but using a div tag instead
    """

    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'class': 'text_area_div'}
        if attrs:
            default_attrs.update(attrs)
        super(TextAreaDiv, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = u''

        flat_attrs = flatatt(self.build_attrs(attrs, name=name))
        content = conditional_escape(force_unicode(value))
        result = u'<pre%s>%s</pre>' % (flat_attrs, content)
        return mark_safe(result)


# From: http://www.peterbe.com/plog/emailinput-html5-django
class EmailInput(forms.widgets.Input):
    """
    Class for a login form widget that accepts only well formated
    email address
    """
    input_type = 'email'

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs.update(dict(autocorrect='off',
                          autocapitalize='off',
                          spellcheck='false'))
        return super(EmailInput, self).render(name, value, attrs=attrs)


class ScrollableCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    """
    Class for a form widget composed of a selection of checkboxes wrapped
    in a div tag with automatic overflow to add scrollbars when the list
    exceds the height of the div
    """
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul class="undecorated_list" style="margin-left: 5px; margin-top: 3px; margin-bottom: 3px;">']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.widgets.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
        output.append(u'</ul>')

        return mark_safe(u'<div class="text_area_div">%s</div>' % u'\n'.join(output))
