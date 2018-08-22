from __future__ import absolute_import, unicode_literals

from django import forms
from django.apps import apps
from django.template.loader import render_to_string
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .permissions import permission_tag_view


class TagFormWidget(forms.SelectMultiple):
    option_template_name = 'tags/forms/widgets/tag_select_option.html'

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset')
        return super(TagFormWidget, self).__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        result = super(TagFormWidget, self).create_option(
            name=name, value=value, label='{}'.format(conditional_escape(label)),
            selected=selected, index=index, subindex=subindex, attrs=attrs
        )

        result['attrs']['data-color'] = self.queryset.get(pk=value).color

        return result


def widget_document_tags(document, user):
    """
    A tag widget that displays the tags for the given document
    """
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )

    result = ['<div class="tag-container">']

    tags = AccessControlList.objects.filter_by_access(
        permission_tag_view, user, queryset=document.attached_tags().all()
    )

    for tag in tags:
        result.append(widget_single_tag(tag))

    result.append('</div>')

    return mark_safe(''.join(result))


def widget_single_tag(tag):
    return render_to_string('tags/tag_widget.html', {'tag': tag})
