from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.utils.html import escape
from django.utils.safestring import mark_safe

from acls.models import AccessControlList
from permissions import Permission

from .permissions import permission_tag_view


def widget_document_tags(document, user):
    """
    A tag widget that displays the tags for the given document
    """
    tags_template = []

    tags = document.attached_tags().all()

    try:
        Permission.check_permissions(user, (permission_tag_view,))
    except PermissionDenied:
        tags = AccessControlList.objects.filter_by_access(
            permission_tag_view, user, tags
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
