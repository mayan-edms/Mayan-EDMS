import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.common.menus import menu_list_facet

from .layers import layer_redactions
from .transformations import *  # NOQA
from .permissions import (
    permission_redaction_create, permission_redaction_delete,
    permission_redaction_edit, permission_redaction_view
)

logger = logging.getLogger(name=__name__)


class RedactionsApp(MayanAppConfig):
    app_namespace = 'redactions'
    app_url = 'redactions'
    has_rest_api = False
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.redactions'
    static_media_ignore_patterns = (
        'redactions/node_modules/cropperjs/src/*',
        'redactions/node_modules/cropperjs/types/index.d.ts',
        'redactions/node_modules/jquery-cropper/src/*',
    )
    verbose_name = _('Redactions')

    def ready(self):
        super().ready()

        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        DocumentFilePage = apps.get_model(
            app_label='documents', model_name='DocumentFilePage'
        )
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )
        DocumentVersionPage = apps.get_model(
            app_label='documents', model_name='DocumentVersionPage'
        )

        ModelPermission.register(
            model=DocumentFile, permissions=(
                permission_redaction_create,
                permission_redaction_delete,
                permission_redaction_edit,
                permission_redaction_view
            )
        )
        ModelPermission.register(
            model=DocumentVersion, permissions=(
                permission_redaction_create,
                permission_redaction_delete,
                permission_redaction_edit,
                permission_redaction_view
            )
        )

        link_redaction_list = link_transformation_list.copy(
            layer=layer_redactions
        )
        link_redaction_list.text = _('Redactions')

        menu_list_facet.bind_links(
            links=(link_redaction_list,), sources=(
                DocumentFilePage, DocumentVersionPage,
            )
        )
