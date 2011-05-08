from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.db import models

from common.utils import return_attrib


class DetailSelectMultiple(forms.widgets.SelectMultiple):
    def __init__(self, queryset=None, *args, **kwargs):
        self.queryset = queryset
        super(DetailSelectMultiple, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
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


class PlainWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % value)


class DetailForm(forms.ModelForm):
    def __init__(self, extra_fields=None, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        if extra_fields:
            for extra_field in extra_fields:
                result = return_attrib(self.instance, extra_field['field'])
                label = 'label' in extra_field and extra_field['label'] or None
                #TODO: Add others result types <=> Field types
                if isinstance(result, models.query.QuerySet):
                    self.fields[extra_field['field']] = \
                        forms.ModelMultipleChoiceField(
                            queryset=result, label=label)
                else:
                    self.fields[extra_field['field']] = forms.CharField(
                        label=extra_field['label'],
                        initial=return_attrib(self.instance,
                            extra_field['field'], None),
                            widget=PlainWidget)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.SelectMultiple):
                self.fields[field_name].widget = DetailSelectMultiple(
                    choices=field.widget.choices,
                    attrs=field.widget.attrs,
                    queryset=getattr(field, 'queryset', None),
                )
                self.fields[field_name].help_text = ''
            elif isinstance(field.widget, forms.widgets.Select):
                self.fields[field_name].widget = DetailSelectMultiple(
                    choices=field.widget.choices,
                    attrs=field.widget.attrs,
                    queryset=getattr(field, 'queryset', None),
                )
                self.fields[field_name].help_text = ''

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs.update({'readonly': 'readonly'})


class GenericConfirmForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pass


class GenericAssignRemoveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        left_list_qryset = kwargs.pop('left_list_qryset', None)
        right_list_qryset = kwargs.pop('right_list_qryset', None)
        left_filter = kwargs.pop('left_filter', None)
        super(GenericAssignRemoveForm, self).__init__(*args, **kwargs)
        if left_filter:
            self.fields['left_list'].queryset = left_list_qryset.filter(
                *left_filter)
        else:
            self.fields['left_list'].queryset = left_list_qryset

        self.fields['right_list'].queryset = right_list_qryset

    left_list = forms.ModelMultipleChoiceField(required=False, queryset=None)
    right_list = forms.ModelMultipleChoiceField(required=False, queryset=None)


class FilterForm(forms.Form):
    def __init__(self, list_filters, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        for list_filter in list_filters:
            label = list_filter.get('title', list_filter['name'])
            self.fields[list_filter['name']] = forms.ModelChoiceField(
                queryset=list_filter['queryset'],
                label=label[0].upper() + label[1:], required=False)
                

class ChoiceForm(forms.Form):
    """
    Form to be used in side by side templates used to add or remove
    items from a many to many field
    """
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        label = kwargs.pop('label', _(u'Selection'))
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['selection'].choices = choices
        self.fields['selection'].label = label
        self.fields['selection'].widget.attrs.update({'size': 14, 'class': 'choice_form'})

    selection = forms.MultipleChoiceField()
