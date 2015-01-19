from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace='permissions',
    module='permissions.settings',
    settings=[
        {'name': 'DEFAULT_ROLES', 'global_name': 'ROLES_DEFAULT_ROLES', 'default': [], 'description': _('A list of existing roles that are automatically assigned to newly created users')},
    ]
)
