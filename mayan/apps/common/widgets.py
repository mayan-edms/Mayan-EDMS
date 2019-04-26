from __future__ import unicode_literals

from django import forms
from django.utils.safestring import mark_safe


class DisableableSelectWidget(forms.widgets.SelectMultiple):
    def create_option(self, *args, **kwargs):
        result = super(DisableableSelectWidget, self).create_option(*args, **kwargs)

        # Get a keyword argument named value or the second positional argument
        # Current interface as of Django 1.11
        # def create_option(self, name, value, label, selected, index,
        # subindex=None, attrs=None):
        value = kwargs.get('value', args[1])

        if value in self.disabled_choices:
            result['attrs'].update({'disabled': 'disabled'})

        return result


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

        attrs.update(
            {
                'autocorrect': 'off',
                'autocapitalize': 'off',
                'spellcheck': 'false'
            }
        )

        return super(EmailInput, self).render(name, value, attrs=attrs)


class PlainWidget(forms.widgets.Widget):
    """
    Class to define a form widget that effectively nulls the htmls of a
    widget and reduces the output to only it's value
    """
    def render(self, name, value, attrs=None):
        return mark_safe(s='%s' % value)


class TextAreaDiv(forms.widgets.Widget):
    """
    Class to define a form widget that simulates the behavior of a
    Textarea widget but using a div tag instead
    """
    template_name = 'appearance/forms/widgets/textareadiv.html'

    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'class': 'text_area_div'}
        if attrs:
            default_attrs.update(attrs)
        super(TextAreaDiv, self).__init__(default_attrs)
