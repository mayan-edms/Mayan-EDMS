from collections import OrderedDict

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


class NamedMultiWidget(forms.widgets.Widget):
    subwidgets = None
    subwidgets_order = None
    template_name = 'django/forms/widgets/multiwidget.html'

    def __init__(self, attrs=None):
        self.widgets = {}
        for name, widget in OrderedDict(self.subwidgets).items():
            self.widgets[name] = widget() if isinstance(widget, type) else widget

        if not self.subwidgets_order:
            self.subwidgets_order = list(self.widgets.keys())

        super(NamedMultiWidget, self).__init__(attrs)

    def _get_media(self):
        "Media for a multiwidget is the combination of all media of the subwidgets"
        media = forms.widgets.Media()
        for name, widget in self.widgets.items():
            media = media + widget.media
        return media
    media = property(_get_media)

    @property
    def is_hidden(self):
        return all(widget.is_hidden for name, widget in self.widgets.items())

    def get_context(self, name, value, attrs):
        context = super(NamedMultiWidget, self).get_context(name, value, attrs)
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        value = self.decompress(value)

        final_attrs = context['widget']['attrs']
        input_type = final_attrs.pop('type', None)
        id_ = final_attrs.get('id')
        subwidgets = []

        # Include new subwidgets added by subclasses after __init__
        _subwidgets_order = self.subwidgets_order.copy()
        for widget in self.widgets.keys():
            if widget not in _subwidgets_order:
                _subwidgets_order.append(widget)

        for subwidget_entry in _subwidgets_order:
            widget_name = subwidget_entry
            widget = self.widgets[widget_name]
            if input_type is not None:
                widget.input_type = input_type
            full_widget_name = '%s_%s' % (name, widget_name)
            try:
                widget_value = value[widget_name]
            except IndexError:
                widget_value = None
            if id_:
                widget_attrs = final_attrs.copy()
                widget_attrs['id'] = '%s_%s' % (id_, widget_name)
            else:
                widget_attrs = final_attrs
            subwidgets.append(
                widget.get_context(
                    full_widget_name, widget_value, widget_attrs
                )['widget']
            )
        context['widget']['subwidgets'] = subwidgets
        return context

    def id_for_label(self, id_):
        if id_:
            id_ += '_{}'.format(list(self.widgets.keys())[0])
        return id_

    def value_from_datadict(self, data, files, name):
        return {
            name: widget.value_from_datadict(
                data, files, name + '_%s' % name
            ) for name, widget in self.widgets.items()
        }

    def value_omitted_from_data(self, data, files, name):
        return all(
            widget.value_omitted_from_data(data, files, name + '_%s' % name)
            for name, widget in self.widgets.items()
        )

    @property
    def needs_multipart_form(self):
        return any(
            widget.needs_multipart_form for name, widget in self.widgets.items()
        )


class PlainWidget(forms.widgets.Widget):
    """
    Class to define a form widget that effectively nulls the htmls of a
    widget and reduces the output to only it's value
    """
    def render(self, name, value, attrs=None, renderer=None):
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
