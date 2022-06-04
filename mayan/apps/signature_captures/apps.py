from django.apps import apps
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary
)
from mayan.apps.databases.classes import ModelFieldRelated
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.rest_api.fields import DynamicSerializerField

from .events import (
    event_signature_capture_created, event_signature_capture_deleted,
    event_signature_capture_edited
)
from .handlers import handler_signature_capture_cache_create
from .links import (
    link_signature_capture_create, link_signature_capture_delete,
    link_signature_capture_edit, link_signature_capture_list
)
from .permissions import (
    permission_signature_capture_create, permission_signature_capture_delete,
    permission_signature_capture_edit, permission_signature_capture_view
)
from .transformations import *  # NOQA


class SignatureCapturesApp(MayanAppConfig):
    app_namespace = 'signature_captures'
    app_url = 'signature_captures'
    has_rest_api = True
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.signature_captures'
    verbose_name = _('Signature captures')

    def ready(self):
        super().ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        SignatureCapture = self.get_model(
            model_name='SignatureCapture'
        )

        DynamicSerializerField.add_serializer(
            klass=SignatureCapture,
            serializer_class='mayan.apps.signature_captures.serializers.SignatureCapture'
        )

        EventModelRegistry.register(model=SignatureCapture)

        ModelEventType.register(
            model=Document, event_types=(
                event_signature_capture_created,
                event_signature_capture_deleted,
                event_signature_capture_edited
            )
        )
        ModelEventType.register(
            model=SignatureCapture, event_types=(
                event_signature_capture_edited,
            )
        )

        ModelFieldRelated(
            model=Document, name='signature_captures__text'
        )
        ModelFieldRelated(
            model=Document, name='signature_captures__internal_name'
        )
        ModelFieldRelated(
            model=Document, name='signature_captures__user__first_name'
        )
        ModelFieldRelated(
            model=Document, name='signature_captures__user__last_name'
        )
        ModelFieldRelated(
            model=Document, name='signature_captures__user__username'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_signature_capture_create,
                permission_signature_capture_delete,
                permission_signature_capture_view
            )
        )

        ModelPermission.register(
            model=SignatureCapture, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_signature_capture_delete,
                permission_signature_capture_edit,
                permission_signature_capture_view
            )
        )

        ModelPermission.register_inheritance(
            model=SignatureCapture, related='document'
        )

        # SignatureCapture

        SourceColumn(
            attribute='date_time_created', is_identifier=True,
            is_sortable=True, source=SignatureCapture
        )
        SourceColumn(
            attribute='date_time_edited', is_sortable=True,
            source=SignatureCapture
        )
        SourceColumn(
            attribute='text', is_sortable=True,
            source=SignatureCapture
        )
        SourceColumn(
            attribute='internal_name', is_sortable=True,
            source=SignatureCapture
        )
        SourceColumn(
            attribute='user', is_sortable=True,
            source=SignatureCapture
        )

        # Document

        menu_list_facet.bind_links(
            links=(link_signature_capture_list,), sources=(Document,)
        )

        menu_object.bind_links(
            links=(
                link_signature_capture_edit,
                link_signature_capture_delete
            ),
            sources=(SignatureCapture,)
        )

        menu_secondary.bind_links(
            links=(link_signature_capture_create, link_signature_capture_list),
            sources=(
                SignatureCapture,
                'signature_captures:signature_capture_create',
                'signature_captures:signature_capture_list',
            )
        )

        post_migrate.connect(
            dispatch_uid='signature_captures_handler_signature_capture_cache_create',
            receiver=handler_signature_capture_cache_create
        )
