from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_setup, menu_object
from common.utils import encapsulate
from common.widgets import exists_widget
from navigation.api import register_model_list_columns

from .classes import Namespace, Setting
from .links import link_check_settings, link_namespace_detail
from .widgets import setting_widget


class SmartSettingsApp(MayanAppConfig):
    app_namespace = 'settings'
    app_url = 'settings'
    name = 'smart_settings'
    verbose_name = _('Smart settings')

    def ready(self):
        super(SmartSettingsApp, self).ready()

        menu_object.bind_links(links=(link_namespace_detail,), sources=(Namespace,))
        menu_setup.bind_links(links=(link_check_settings,))

        register_model_list_columns(Namespace, [
            {
                'name': _('Setting count'),
                'attribute': encapsulate(lambda instance: len(instance.settings))
            },
        ])

        register_model_list_columns(Setting, [
            {
                'name': _('Name'),
                'attribute': encapsulate(lambda instance: setting_widget(instance))
            },
            {
                'name': _('Value'), 'attribute': 'value'
            },
            {
                'name': _('Found in path'), 'attribute': encapsulate(lambda instance: exists_widget(instance.value) if instance.is_path else _('n/a'))
            },
        ])
