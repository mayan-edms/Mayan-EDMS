from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .icons import icon_permissions
from .links import role_list
from .cleanup import cleanup

name = 'permissions'
label = _(u'Permissions')
description = _(u'Handles the permissions in a project.')
icon = icon_permissions
dependencies = ['app_registry', 'smart_settings']
bootstrap_models = [
    {
        'name': 'role',
    },
]
cleanup_functions = [cleanup]
settings = [
    {
        'name': 'DEFAULT_ROLES',
        'default': [],
        'description': _(u'A list of existing roles that are automatically assigned to newly created users'),
        'scopes': [LocalScope()]
    }
]

setup_links = [role_list]
