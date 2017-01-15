from __future__ import absolute_import, unicode_literals

from django import forms
from django.apps import apps
from django.utils.html import escape
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .permissions import permission_tag_view


class TagFormWidget(forms.SelectMultiple):
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset')
        return super(TagFormWidget, self).__init__(*args, **kwargs)

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
        return format_html(
            '<option style="color:{};" value="{}"{}>{}</option>',
            self.queryset.get(pk=option_value).color,
            option_value,
            selected_html,
            force_text(option_label)
        )


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
    return mark_safe(
        '''
            <span class="label label-tag" style="background: {}">{}</span>
        '''.format(tag.color, escape(tag.label).replace(' ', '&nbsp;'))
    )
