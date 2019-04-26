from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_facet, menu_object, menu_secondary
from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.events import ModelEventType
from mayan.apps.navigation import SourceColumn

from .events import (
    event_document_comment_create, event_document_comment_delete
)
from .links import (
    link_comment_add, link_comment_delete, link_comments_for_document
)
from .permissions import (
    permission_comment_create, permission_comment_delete,
    permission_comment_view
)


class DocumentCommentsApp(MayanAppConfig):
    app_namespace = 'comments'
    app_url = 'comments'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_comments'
    verbose_name = _('Document comments')

    def ready(self):
        super(DocumentCommentsApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        Comment = self.get_model(model_name='Comment')

        ModelEventType.register(
            model=Document, event_types=(
                event_document_comment_create, event_document_comment_delete
            )
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_comment_create, permission_comment_delete,
                permission_comment_view
            )
        )

        SourceColumn(attribute='submit_date', source=Comment)
        SourceColumn(
            func=lambda context: context['object'].user.get_full_name() if context['object'].user.get_full_name() else context['object'].user,
            source=Comment
        )
        SourceColumn(attribute='comment', source=Comment)

        document_page_search.add_model_field(
            field='document_version__document__comments__comment',
            label=_('Comments')
        )
        document_search.add_model_field(
            field='comments__comment',
            label=_('Comments')
        )

        menu_secondary.bind_links(
            links=(link_comment_add,),
            sources=(
                'comments:comments_for_document', 'comments:comment_add',
                'comments:comment_delete', 'comments:comment_multiple_delete'
            )
        )
        menu_object.bind_links(
            links=(link_comment_delete,), sources=(Comment,)
        )
        menu_facet.bind_links(
            links=(link_comments_for_document,), sources=(Document,)
        )
