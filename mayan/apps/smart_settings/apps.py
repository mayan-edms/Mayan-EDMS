from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_setup, menu_object
from common.utils import encapsulate
from common.widgets import exists_widget
from navigation import SourceColumn

from .classes import Namespace, Setting
from .links import link_namespace_detail, link_namespace_list
from .widgets import setting_widget


class SmartSettingsApp(MayanAppConfig):
    app_namespace = 'settings'
    app_url = 'settings'
    name = 'smart_settings'
    verbose_name = _('Smart settings')

    def ready(self):
        super(SmartSettingsApp, self).ready()

        SourceColumn(source=Namespace, label=_('Setting count'), attribute=encapsulate(lambda instance: len(instance.settings)))
        SourceColumn(source=Setting, label=_('Name'), attribute=encapsulate(lambda instance: setting_widget(instance)))
        SourceColumn(source=Setting, label=_('Value'), attribute='serialized_value')
        SourceColumn(source=Setting, label=_('Found in path'), attribute=encapsulate(lambda instance: exists_widget(instance.value) if instance.is_path else _('n/a')))

        menu_object.bind_links(links=(link_namespace_detail,), sources=(Namespace,))
        menu_setup.bind_links(links=(link_namespace_list,))
