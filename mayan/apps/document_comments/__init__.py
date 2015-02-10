from __future__ import absolute_import, unicode_literals

from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.classes import ModelAttribute
from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_links, register_model_list_columns

from .links import comment_add, comment_delete, comments_for_document
from .permissions import (
    PERMISSION_COMMENT_CREATE, PERMISSION_COMMENT_DELETE,
    PERMISSION_COMMENT_VIEW
)


Document.add_to_class(
    'comments',
    generic.GenericRelation(
        Comment,
        content_type_field='content_type',
        object_id_field='object_pk'
    )
)

class_permissions(Document, [PERMISSION_COMMENT_CREATE,
                             PERMISSION_COMMENT_DELETE,
                             PERMISSION_COMMENT_VIEW])

register_model_list_columns(Comment, [
    {
        'name': _('Date'),
        'attribute': 'submit_date'
    },
    {
        'name': _('User'),
        'attribute': encapsulate(lambda x: x.user.get_full_name() if x.user.get_full_name() else x.user)
    },
    {
        'name': _('Comment'),
        'attribute': 'comment'
    }
])

register_links(['comments:comments_for_document', 'comments:comment_add', 'comments:comment_delete', 'comments:comment_multiple_delete'], [comment_add], menu_name='sidebar')
register_links(Comment, [comment_delete])
register_links(Document, [comments_for_document], menu_name='form_header')

ModelAttribute(Document, label=_('Comments'), name='comments', type_name='related')
