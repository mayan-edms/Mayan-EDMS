from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import menu_secondary, menu_setup, menu_object
from mayan.apps.navigation.classes import SourceColumn

from .classes import Namespace, Setting
from .links import (
    link_namespace_detail, link_namespace_list, link_namespace_root_list,
    link_setting_edit
)
from .widgets import setting_widget


class SmartSettingsApp(MayanAppConfig):
    app_namespace = 'settings'
    app_url = 'settings'
    has_tests = True
    name = 'mayan.apps.smart_settings'
    verbose_name = _('Smart settings')

    def ready(self):
        super(SmartSettingsApp, self).ready()

        Namespace.initialize()

        SourceColumn(
            source=Namespace, label=_('Setting count'),
            func=lambda context: len(context['object'].settings)
        )
        SourceColumn(
            source=Setting, label=_('Name'),
            func=lambda context: setting_widget(context['object'])
        )
        SourceColumn(
            attribute='serialized_value', label=_('Value'), source=Setting
        )
        SourceColumn(
            attribute='is_overridden', source=Setting, widget=TwoStateWidget
        )

        menu_object.bind_links(
            links=(link_namespace_detail,), sources=(Namespace,)
        )
        menu_object.bind_links(
            links=(link_setting_edit,), sources=(Setting,)
        )
        menu_secondary.bind_links(
            links=(link_namespace_root_list,), sources=(
                Namespace, Setting, 'settings:namespace_list',
            )
        )
        menu_setup.bind_links(links=(link_namespace_list,))

        Setting.save_last_known_good()
