from __future__ import unicode_literals

import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import (
    MayanAppConfig, menu_facet, menu_object, menu_secondary, menu_sidebar
)
from common.widgets import two_state_template
from navigation import SourceColumn

from .links import (
    link_document_version_signature_delete,
    link_document_version_signature_details,
    link_document_version_signature_download,
    link_document_version_signature_list,
    link_document_version_signature_upload,
    link_document_version_signature_verify
)
from .permissions import (
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
    permission_document_version_signature_verify,
    permission_document_version_signature_view,
)

logger = logging.getLogger(__name__)


class DocumentSignaturesApp(MayanAppConfig):
    app_namespace = 'signatures'
    app_url = 'signatures'
    name = 'document_signatures'
    test = True
    verbose_name = _('Document signatures')

    def ready(self):
        super(DocumentSignaturesApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        DetachedSignature = self.get_model('DetachedSignature')

        EmbeddedSignature = self.get_model('EmbeddedSignature')

        SignatureBaseModel = self.get_model('SignatureBaseModel')

        DocumentVersion.register_post_save_hook(
            order=1, func=EmbeddedSignature.objects.check_signature
        )
        DocumentVersion.register_pre_open_hook(
            order=1, func=EmbeddedSignature.objects.open_signed
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_version_signature_delete,
                permission_document_version_signature_download,
                permission_document_version_signature_verify,
                permission_document_version_signature_view,
                permission_document_version_signature_upload,
            )
        )

        SourceColumn(
            source=SignatureBaseModel, label=_('Date'), attribute='date'
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Key ID'), attribute='key_id'
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Signature ID'),
            func=lambda context: context['object'].signature_id or _('None')
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Public key ID'),
            func=lambda context: context['object'].public_key_fingerprint or _('None')
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Is embedded?'),
            func=lambda context: two_state_template(
                SignatureBaseModel.objects.get_subclass(
                    pk=context['object'].pk
                ).is_embedded
            )
        )
        SourceColumn(
            source=SignatureBaseModel, label=_('Is detached?'),
            func=lambda context: two_state_template(
                SignatureBaseModel.objects.get_subclass(
                    pk=context['object'].pk
                ).is_detached
            )
        )

        menu_object.bind_links(
            links=(link_document_version_signature_list,),
            sources=(DocumentVersion,)
        )
        menu_object.bind_links(
            links=(
                link_document_version_signature_details,
                link_document_version_signature_download,
                link_document_version_signature_delete,
            ), sources=(SignatureBaseModel,)
        )
        menu_sidebar.bind_links(
            links=(
                link_document_version_signature_upload,
                link_document_version_signature_verify,
            ), sources=(DocumentVersion,)
        )
