from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic

from navigation.api import register_links, register_model_list_columns
from common.utils import encapsulate
from acls.api import class_permissions
from documents.models import Document

if 'django.contrib.comments' not in settings.INSTALLED_APPS:
    raise Exception('This app depends on the django.contrib.comments app.')

from .permissions import (PERMISSION_COMMENT_CREATE,
    PERMISSION_COMMENT_DELETE, PERMISSION_COMMENT_VIEW)

comment_delete = {'text': _('delete'), 'view': 'comment_delete', 'args': 'object.pk', 'famfam': 'comment_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_multiple_delete = {'text': _('delete'), 'view': 'comment_multiple_delete', 'args': 'object.pk', 'famfam': 'comments_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_add = {'text': _('add comment'), 'view': 'comment_add', 'args': 'object.pk', 'famfam': 'comment_add', 'permissions': [PERMISSION_COMMENT_CREATE]}
comments_for_document = {'text': _('comments'), 'view': 'comments_for_document', 'args': 'object.pk', 'famfam': 'comments', 'permissions': [PERMISSION_COMMENT_VIEW], 'children_view_regex': ['comment']}

register_model_list_columns(Comment, [
    {
        'name': _(u'date'),
        'attribute': 'submit_date'
    },
    {
        'name': _(u'user'),
        'attribute': encapsulate(lambda x: x.user.get_full_name() if x.user.get_full_name() else x.user)
    },
    {
        'name': _(u'comment'),
        'attribute': 'comment'
    }
])

register_links(['comments_for_document', 'comment_add', 'comment_delete', 'comment_multiple_delete'], [comment_add], menu_name='sidebar')
register_links(Comment, [comment_delete])
register_links(Document, [comments_for_document], menu_name='form_header')


def flat_comments(document):
    return u' '.join(document.comments.values_list('comment', flat=True))


Document.add_to_class(
    'comments',
    generic.GenericRelation(
        Comment,
        content_type_field='content_type',
        object_id_field='object_pk'
    )
)

Document.add_to_class('flat_comments', flat_comments)

class_permissions(Document, [
    PERMISSION_COMMENT_CREATE,
    PERMISSION_COMMENT_DELETE,
    PERMISSION_COMMENT_VIEW
])
