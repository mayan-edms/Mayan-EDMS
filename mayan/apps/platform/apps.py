from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.db.models.signals import m2m_changed, pre_delete
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelField
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_secondary
)
from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

"""
from .dependencies import *  # NOQA
from .events import (
    event_tag_attach, event_tag_created, event_tag_edited, event_tag_remove
)
from .handlers import handler_index_document, handler_tag_pre_delete
from .html_widgets import widget_document_tags
from .links import (
    link_document_tag_list, link_document_multiple_attach_multiple_tag,
    link_document_multiple_tag_multiple_remove,
    link_document_tag_multiple_remove, link_document_tag_multiple_attach, link_tag_create,
    link_tag_delete, link_tag_edit, link_tag_list,
    link_tag_multiple_delete, link_tag_document_list
)
from .menus import menu_tags
from .methods import method_document_get_tags
from .permissions import (
    permission_tag_attach, permission_tag_delete, permission_tag_edit,
    permission_tag_remove, permission_tag_view
)
from .search import tag_search  # NOQA
"""
#from mayan.apps.common.classes import Template
from mayan.apps.task_manager.classes import Worker


class PlatformTemplate(object):
    _registry = {}
    context = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, template_name):
        self.name = name
        self.template_name = template_name
        self.__class__._registry[name] = self

    def get_context(self):
        return self.context

    def render(self):
        from django.template import loader
        return loader.render_to_string(
            template_name=self.template_name,
            context=self.get_context()
        )



class PlatformTemplateSupervisord(PlatformTemplate):
    def get_context(self):
        return {'workers': Worker.all()}


class PlatformApp(MayanAppConfig):
    app_namespace = 'platform'
    app_url = 'platform'
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.platform'
    verbose_name = _('Platform')

    def ready(self):
        super(PlatformApp, self).ready()

        t = PlatformTemplateSupervisord(
            name='platform_supervisord',
            template_name='platform/supervisord.html'
        )

        print ("#@#@", t.render())
        print("!!!!", Worker.all())
