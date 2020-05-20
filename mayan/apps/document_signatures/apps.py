import logging

from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_facet, menu_object, menu_secondary, menu_tools
)
from mayan.apps.navigation.classes import SourceColumn

from .handlers import (
    handler_unverify_key_signatures, handler_verify_key_signatures
)
from .hooks import (
    hook_create_embedded_signature, hook_decrypt_document_version
)
from .links import (
    link_document_version_all_signature_verify,
    link_document_signature_list,
    link_document_version_signature_delete,
    link_document_version_signature_detached_create,
    link_document_version_signature_embedded_create,
    link_document_version_signature_details,
    link_document_version_signature_download,
    link_document_version_signature_list,
    link_document_version_signature_upload,
)
from .permissions import (
    permission_document_version_sign_detached,
    permission_document_version_sign_embedded,
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
    permission_document_version_signature_view,
)

logger = logging.getLogger(name=__name__)


class DocumentSignaturesApp(MayanAppConfig):
    app_namespace = 'signatures'
    app_url = 'signatures'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.document_signatures'
    verbose_name = _('Document signatures')

    def ready(self):
        super(DocumentSignaturesApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        Key = apps.get_model(
            app_label='django_gpg', model_name='Key'
        )

        DetachedSignature = self.get_model(model_name='DetachedSignature')

        SignatureBaseModel = self.get_model(model_name='SignatureBaseModel')

        DocumentVersion.register_post_save_hook(
            func=hook_create_embedded_signature, order=1
        )
        DocumentVersion.register_pre_open_hook(
            func=hook_decrypt_document_version, order=1
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_version_sign_detached,
                permission_document_version_sign_embedded,
                permission_document_version_signature_delete,
                permission_document_version_signature_download,
                permission_document_version_signature_view,
                permission_document_version_signature_upload,
            )
        )
        ModelPermission.register_inheritance(
            model=SignatureBaseModel, related='document_version'
        )
        ModelPermission.register_inheritance(
            model=DetachedSignature, related='document_version'
        )

        SourceColumn(
            source=SignatureBaseModel, label=_('Date'), attribute='date'
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Key ID'),
            attribute='get_key_id'
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Signature ID'),
            func=lambda context: context['object'].signature_id or _('None')
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Type'),
            func=lambda context: SignatureBaseModel.objects.get_subclass(
                pk=context['object'].pk
            ).get_signature_type_display()
        )

        menu_facet.bind_links(
            links=(link_document_signature_list,), sources=(Document,)
        )
        menu_facet.bind_links(
            links=(
                link_document_version_signature_list,
            ), position=9, sources=(DocumentVersion,)
        )

        menu_object.bind_links(
            links=(
                link_document_version_signature_detached_create,
                link_document_version_signature_embedded_create
            ), sources=(DocumentVersion,)
        )
        menu_object.bind_links(
            links=(
                link_document_version_signature_details,
                link_document_version_signature_download,
                link_document_version_signature_delete,
            ), sources=(SignatureBaseModel,)
        )
        menu_secondary.bind_links(
            links=(
                link_document_version_signature_upload,
            ), sources=(DocumentVersion,)
        )
        menu_tools.bind_links(
            links=(link_document_version_all_signature_verify,)
        )

        post_delete.connect(
            dispatch_uid='signatures_handler_unverify_key_signatures',
            receiver=handler_unverify_key_signatures,
            sender=Key
        )
        post_save.connect(
            dispatch_uid='signatures_handler_verify_key_signatures',
            receiver=handler_verify_key_signatures,
            sender=Key
        )
