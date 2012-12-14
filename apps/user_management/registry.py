from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from smart_settings import LocalScope

from .icons import icon_user
from .links import user_setup, group_setup
from .cleanup import delete_users_and_groups

label = _(u'User management')
description = _(u'Handles user accounts and groups.')
icon = icon_user
dependencies = ['app_registry', 'icons', 'navigation', 'permissions']
setup_links = [user_setup, group_setup]
cleanup_functions = [delete_users_and_groups]

settings=[
    {
        'name': 'AUTO_CREATE_ADMIN',
        'default': True,
        'description': _(u'Automatically create a superuser admin on the first run.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'AUTO_ADMIN_USERNAME',
        'default': 'admin',
        'description': _(u'User name of the superuser admin that will be created.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'AUTO_ADMIN_PASSWORD',
        'default': User.objects.make_random_password(),
        'description': _(u'Password of the superuser admin that will be created.'),
        'scopes': [LocalScope()]
    }
]
