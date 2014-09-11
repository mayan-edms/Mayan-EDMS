"""Configuration options for the permissions app"""
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'permissions',
    module=u'permissions.settings',
    settings=[
        {'name': u'DEFAULT_ROLES', 'global_name': u'ROLES_DEFAULT_ROLES', 'default': [], 'description': _('A list of existing roles that are automatically assigned to newly created users')},
    ]
)
