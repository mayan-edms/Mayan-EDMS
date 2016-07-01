from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

from .literals import (
    DEFAULT_ORGANIZATION_ADMIN_EMAIL, DEFAULT_ORGANIZATION_ADMIN_GROUP,
    DEFAULT_ORGANIZATION_ADMIN_PASSWORD, DEFAULT_ORGANIZATION_ADMIN_ROLE,
    DEFAULT_ORGANIZATION_ADMIN_USERNAME
)


namespace = Namespace(name='organizations', label=_('Organizations'))
setting_organization_admin_email = namespace.add_setting(
    global_name='ORGANIZATIONS_ADMIN_EMAIL',
    default=DEFAULT_ORGANIZATION_ADMIN_EMAIL,
    help_text=_('Email to use when creating organization admin users.')
)
setting_organization_admin_group = namespace.add_setting(
    global_name='ORGANIZATIONS_ADMIN_GROUP',
    default=DEFAULT_ORGANIZATION_ADMIN_GROUP, help_text=_(
        'Group to use when creating organization admin users.'
    ),
)
setting_organization_admin_password = namespace.add_setting(
    global_name='ORGANIZATIONS_ADMIN_PASSWORD',
    default=DEFAULT_ORGANIZATION_ADMIN_PASSWORD,
    help_text=_(
        'Password to use when creating organization admin users. If none is '
        'specified a random password will be generated.'
    )
)
setting_organization_admin_role = namespace.add_setting(
    global_name='ORGANIZATIONS_ADMIN_ROLE',
    default=DEFAULT_ORGANIZATION_ADMIN_ROLE, help_text=_(
        'Role to use when creating organization admin users.'
    ),
)
setting_organization_admin_username = namespace.add_setting(
    global_name='ORGANIZATIONS_ADMIN_USERNAME',
    default=DEFAULT_ORGANIZATION_ADMIN_USERNAME, help_text=_(
        'Username to use when creating organization admin users.'
    ),
)
