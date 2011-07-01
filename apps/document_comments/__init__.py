from django.utils.translation import ugettext_lazy as _
from django.conf import settings 
from django.contrib.comments.models import Comment

from navigation.api import register_links, \
    register_model_list_columns
from permissions.api import register_permission, set_namespace_title

from documents.models import Document

if 'django.contrib.comments' not in settings.INSTALLED_APPS:
    raise Exception('This app depends on the django.contrib.comments app.')

PERMISSION_COMMENT_CREATE = {'namespace': 'comments', 'name': 'comment_create', 'label': _(u'Create new comments')}
PERMISSION_COMMENT_DELETE = {'namespace': 'comments', 'name': 'comment_delete', 'label': _(u'Delete comments')}
PERMISSION_COMMENT_EDIT = {'namespace': 'comments', 'name': 'comment_edit', 'label': _(u'Edit comments')}
PERMISSION_COMMENT_VIEW = {'namespace': 'comments', 'name': 'comment_view', 'label': _(u'View comments')}

set_namespace_title('comments', _(u'Comments'))
register_permission(PERMISSION_COMMENT_CREATE)
register_permission(PERMISSION_COMMENT_DELETE)
register_permission(PERMISSION_COMMENT_EDIT)
register_permission(PERMISSION_COMMENT_VIEW)

comment_delete = {'text': _('delete'), 'view': 'comment_delete', 'args': 'object.pk', 'famfam': 'comment_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_multiple_delete = {'text': _('delete'), 'view': 'comment_multiple_delete', 'args': 'object.pk', 'famfam': 'comments_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_add = {'text': _('add comment'), 'view': 'comment_add', 'args': 'object.pk', 'famfam': 'comment_add', 'permissions': [PERMISSION_COMMENT_CREATE]}
comments_for_object = {'text': _('comments'), 'view': 'comments_for_object', 'args': 'object.pk', 'famfam': 'comments', 'permissions': [PERMISSION_COMMENT_VIEW]}

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

register_links(['comments_for_object', 'comment_add', 'comment_delete', 'comment_multiple_delete'], [comment_add], menu_name='sidebar')
register_links(Comment, [comment_delete])

#comment_views = ['comment_delete', 'comment_multiple_delete', 'comment_add', 'comments_for_object']
register_links(Document, [comments_for_object], menu_name='form_header')
