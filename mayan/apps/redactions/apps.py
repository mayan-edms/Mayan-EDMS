from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_multi_item, menu_object, menu_secondary,
    menu_tools
)
from mayan.apps.navigation.classes import SourceColumn

from .handlers import handler_create_default_full_zone
from .links import (
    link_redaction_create, link_redaction_edit, link_redaction_list
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

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )
        Redaction = self.get_model(model_name='Redaction')
        Transformation = apps.get_model(
            app_label='converter', model_name='Transformation'
        )

        #columns = SourceColumn.get_for_source(context=None, source=Transformation)
        #print("@@@", columns)

        menu_list_facet.bind_links(
            links=(
                link_redaction_list,
            ), sources=(DocumentPage,)
        )
        menu_object.bind_links(
            links=(link_redaction_edit,), sources=(Transformation,)
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
