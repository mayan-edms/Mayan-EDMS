from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, \
    register_model_list_columns
from permissions.api import register_permissions

from django.contrib.comments.models import Comment

from documents.models import Document

PERMISSION_COMMENT_CREATE = 'comment_create'
PERMISSION_COMMENT_DELETE = 'comment_delete'
PERMISSION_COMMENT_EDIT = 'comment_edit'

register_permissions('comments', [
    {'name': PERMISSION_COMMENT_CREATE, 'label': _(u'Create new comments')},
    {'name': PERMISSION_COMMENT_DELETE, 'label': _(u'Delete comments')},
    {'name': PERMISSION_COMMENT_EDIT, 'label': _(u'Edit comments')},
])

comment_delete = {'text': _('delete'), 'view': 'comment_delete', 'args': 'object.id', 'famfam': 'comment_delete', 'permissions': {'namespace': 'comments', 'permissions': [PERMISSION_COMMENT_DELETE]}}
comment_multiple_delete = {'text': _('delete'), 'view': 'comment_multiple_delete', 'args': 'object.id', 'famfam': 'comments_delete', 'permissions': {'namespace': 'comments', 'permissions': [PERMISSION_COMMENT_DELETE]}}
comment_add = {'text': _('add comment'), 'view': 'comment_add', 'args': 'document.id', 'famfam': 'comment_add', 'permissions': {'namespace': 'comments', 'permissions': [PERMISSION_COMMENT_CREATE]}}

register_model_list_columns(Comment, [
    {
        'name': _(u'date'),
        'attribute': 'submit_date'
    },
    {
        'name': _(u'user'),
        'attribute': lambda x: x.user.get_full_name() if x.user.get_full_name() else x.user
    },
    {
        'name': _(u'comment'),
        'attribute': 'comment'
    }
])

register_links(Document, [comment_add])
