from __future__ import absolute_import

import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from smart_settings import LocalScope

from .icons import icon_document_signature
from .links import key_setup

name = 'django_gpg'
label = _(u'GPG')
description = _(u'Handles digital signatures.')
icon = icon_document_signature
dependencies = ['app_registry', 'permissions']
setup_links = [key_setup]

settings = [
    {
        'name': 'KEYSERVERS',
        'default': ['pool.sks-keyservers.net'],
        'description': _(u'List of keyservers to be queried for unknown keys.'),
        'scopes': [LocalScope()],
    },
    {
        'name': 'GPG_HOME',
        'default': os.path.join(settings.PROJECT_ROOT, u'gpg_home'),
        'description': _(u'Home directory used to store keys as well as configuration files.'),
        'exists': True,
        'scopes': [LocalScope()],
    }
]
