"""Configuration options for the linking app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('linking', _(u'Linking'), module='linking.conf.settings')

Setting(
    namespace=namespace,
    name='SHOW_EMPTY_SMART_LINKS',
    global_name='LINKING_SHOW_EMPTY_SMART_LINKS',
    default=True,
    description=_(u'Show smart link that don\'t return any documents.')
)
