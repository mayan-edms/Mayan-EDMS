from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .permissions import permission_tag_view


def widget_document_tags(document, user):
    """
    A tag widget that displays the tags for the given document
    """
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )

    tags_template = []

    tags = AccessControlList.objects.filter_by_access(
        permission_tag_view, user, queryset=document.attached_tags().all()
    )

    for tag in tags:
        tags_template.append(widget_single_tag(tag))

    return mark_safe(''.join(tags_template))


def widget_single_tag(tag):
    return mark_safe(
        '''
            <span class="label label-tag" style="background: {}">{}</span>
        '''.format(tag.color, escape(tag.label).replace(' ', '&nbsp;'))
    )
