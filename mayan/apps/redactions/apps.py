import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.converter.links import link_transformation_list
from mayan.apps.common.menus import menu_list_facet

from .layers import layer_redactions
from .transformations import *  # NOQA

logger = logging.getLogger(name=__name__)


class RedactionsApp(MayanAppConfig):
    app_namespace = 'redactions'
    app_url = 'redactions'
    has_rest_api = False
    has_static_media = True
    has_tests = False
    name = 'mayan.apps.redactions'
    static_media_ignore_patterns = (
        'redactions/node_modules/cropperjs/src/*',
        'redactions/node_modules/cropperjs/types/index.d.ts',
        'redactions/node_modules/jquery-cropper/src/*',
    )
    verbose_name = _('Redactions')

    def ready(self):
        super(RedactionsApp, self).ready()

        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )

        link_redaction_list = link_transformation_list.copy(
            layer=layer_redactions
        )
        link_redaction_list.text = _('Redactions')

        menu_list_facet.bind_links(
            links=(link_redaction_list,), sources=(DocumentPage,)
        )
