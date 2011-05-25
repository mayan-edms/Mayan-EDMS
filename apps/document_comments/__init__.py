from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, \
    register_model_list_columns
from permissions.api import register_permission

from django.contrib.comments.models import Comment

from documents.models import Document

PERMISSION_COMMENT_CREATE = {'namespace': 'comments', 'name': 'comment_create', 'label': _(u'Create new comments')}
PERMISSION_COMMENT_DELETE = {'namespace': 'comments', 'name': 'comment_delete', 'label': _(u'Delete comments')}
PERMISSION_COMMENT_EDIT = {'namespace': 'comments', 'name': 'comment_edit', 'label': _(u'Edit comments')}

register_permission(PERMISSION_COMMENT_CREATE)
register_permission(PERMISSION_COMMENT_DELETE)
register_permission(PERMISSION_COMMENT_EDIT)

comment_delete = {'text': _('delete'), 'view': 'comment_delete', 'args': 'object.id', 'famfam': 'comment_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_multiple_delete = {'text': _('delete'), 'view': 'comment_multiple_delete', 'args': 'object.id', 'famfam': 'comments_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_add = {'text': _('add comment'), 'view': 'comment_add', 'args': 'object.id', 'famfam': 'comment_add', 'permissions': [PERMISSION_COMMENT_CREATE]}

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
