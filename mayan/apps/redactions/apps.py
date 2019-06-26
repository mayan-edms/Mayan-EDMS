from __future__ import unicode_literals

import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary,
)

from .links import (
    link_redaction_create, link_redaction_delete, link_redaction_edit,
    link_redaction_list
)

logger = logging.getLogger(__name__)


class RedactionsApp(MayanAppConfig):
    app_namespace = 'redactions'
    app_url = 'redactions'
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.redactions'
    verbose_name = _('Redactions')

    def ready(self):
        super(RedactionsApp, self).ready()

        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )
        Redaction = self.get_model(model_name='Redaction')

        menu_list_facet.bind_links(
            links=(
                link_redaction_list,
            ), sources=(DocumentPage,)
        )
        menu_object.bind_links(
            links=(link_redaction_delete, link_redaction_edit,),
            sources=(Redaction,)
        )
        menu_secondary.bind_links(
            links=(link_redaction_create,), sources=(Redaction,)
        )
        menu_secondary.bind_links(
            links=(link_redaction_create,),
            sources=(
                'redactions:redaction_create',
                'redactions:redaction_list'
            )
        )
