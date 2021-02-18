from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_facet, menu_object, menu_secondary
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

from .events import (
    event_document_comment_created, event_document_comment_deleted,
    event_document_comment_edited
)
from .links import (
    link_comment_add, link_comment_delete, link_comment_edit,
    link_comments_for_document
)
from .permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)


class DocumentCommentsApp(MayanAppConfig):
    app_namespace = 'comments'
    app_url = 'comments'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_comments'
    verbose_name = _('Document comments')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        Comment = self.get_model(model_name='Comment')

        EventModelRegistry.register(model=Comment)

        ModelEventType.register(
            model=Comment, event_types=(
                event_document_comment_edited,
            )
        )
        ModelEventType.register(
            model=Document, event_types=(
                event_document_comment_created, event_document_comment_deleted,
                event_document_comment_edited
            )
        )

        ModelPermission.register(
            model=Comment, permissions=(permission_events_view,)
        )
        ModelPermission.register_inheritance(
            model=Comment, related='document',
        )
        ModelPermission.register(
            model=Document, permissions=(
                permission_document_comment_create,
                permission_document_comment_delete,
                permission_document_comment_edit,
                permission_document_comment_view
            )
        )

        SourceColumn(
            attribute='submit_date', is_identifier=True, is_sortable=True,
            source=Comment
        )
        SourceColumn(
            attribute='get_user_label', is_sortable=True,
            include_label=True, sort_field='user', source=Comment
        )
        SourceColumn(attribute='text', include_label=True, source=Comment)

        menu_facet.bind_links(
            links=(link_comments_for_document,), sources=(Document,)
        )

        menu_secondary.bind_links(
            links=(link_comment_add,),
            sources=(
                'comments:comments_for_document', 'comments:comment_add',
                'comments:comment_delete', 'comments:comment_details',
                'comments:comment_edit', 'comments:comment_multiple_delete'
            )
        )

        menu_object.bind_links(
            links=(link_comment_delete, link_comment_edit), sources=(Comment,)
        )
