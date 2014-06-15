from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import (PERMISSION_COMMENT_CREATE,
    PERMISSION_COMMENT_DELETE, PERMISSION_COMMENT_VIEW)

comment_delete = {'text': _('delete'), 'view': 'comment_delete', 'args': 'object.pk', 'famfam': 'comment_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_multiple_delete = {'text': _('delete'), 'view': 'comment_multiple_delete', 'args': 'object.pk', 'famfam': 'comments_delete', 'permissions': [PERMISSION_COMMENT_DELETE]}
comment_add = {'text': _('add comment'), 'view': 'comment_add', 'args': 'object.pk', 'famfam': 'comment_add', 'permissions': [PERMISSION_COMMENT_CREATE]}
comments_for_document = {'text': _('comments'), 'view': 'comments_for_document', 'args': 'object.pk', 'famfam': 'comments', 'permissions': [PERMISSION_COMMENT_VIEW], 'children_view_regex': ['comment']}
