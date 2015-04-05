from __future__ import absolute_import, unicode_literals

from django import apps
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common import menu_facet, menu_object, menu_sidebar
from common.classes import ModelAttribute
from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_model_list_columns

from .links import (
    link_comment_add, link_comment_delete, link_comments_for_document
)
from .permissions import (
    PERMISSION_COMMENT_CREATE, PERMISSION_COMMENT_DELETE,
    PERMISSION_COMMENT_VIEW
)


class DocumentCommentsApp(apps.AppConfig):
    name = 'document_comments'
    verbose_name = _('Document comments')

    def ready(self):
        Document.add_to_class(
            'comments',
            generic.GenericRelation(
                Comment,
                content_type_field='content_type',
                object_id_field='object_pk'
            )
        )

        ModelAttribute(Document, label=_('Comments'), name='comments', type_name='related')

        class_permissions(Document, [
            PERMISSION_COMMENT_CREATE,
            PERMISSION_COMMENT_DELETE,
            PERMISSION_COMMENT_VIEW]
        )

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

        menu_sidebar.bind_links(links=[link_comment_add], sources=['comments:comments_for_document', 'comments:comment_add', 'comments:comment_delete', 'comments:comment_multiple_delete'])
        menu_object.bind_links(links=[link_comment_delete], sources=[Comment])
        menu_facet.bind_links(links=[link_comments_for_document], sources=[Document])
