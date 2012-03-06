"""Configuration options for the permissions app"""
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('permissions', _(u'Permissions'), module='permissions.conf.settings')

Setting(
    namespace=namespace,
    name='DEFAULT_ROLES',
    global_name='ROLES_DEFAULT_ROLES',
    default=[],
    description=_(u'A list of existing roles that are automatically assigned to newly created users')
)
