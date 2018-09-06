from __future__ import unicode_literals

from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .icons import icon_fail as default_icon_fail, icon_ok as default_icon_ok


class DisableableSelectWidget(forms.SelectMultiple):
    allow_multiple_selected = True

    def __init__(self, *args, **kwargs):
        self.disabled_choices = kwargs.pop('disabled_choices', ())
        super(DisableableSelectWidget, self).__init__(*args, **kwargs)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        if option_value in self.disabled_choices:
            disabled_html = u' disabled="disabled"'
        else:
            disabled_html = ''
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           disabled_html,
                           force_text(option_label))


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


class PlainWidget(forms.widgets.Widget):
    """
    Class to define a form widget that effectively nulls the htmls of a
    widget and reduces the output to only it's value
    """
    def render(self, name, value, attrs=None):
        return mark_safe('%s' % value)


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


class TwoStateWidget(object):
    def __init__(self, state, center=False, icon_ok=None, icon_fail=None):
        self.state = state
        self.icon_ok = icon_ok or default_icon_ok
        self.icon_fail = icon_fail or default_icon_fail
        self.center = center

    def render(self):
        center_class = ''
        if self.center:
            center_class = 'text-center'

        if self.state:
            return mark_safe(
                '<div class="{} text-success">{}</div>'.format(
                    center_class, self.icon_ok.render()
                )
            )
        else:
            return mark_safe(
                '<div class="{} text-danger">{}</div>'.format(
                    center_class, self.icon_fail.render()
                )
            )
