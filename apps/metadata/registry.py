from __future__ import absolute_import

import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from smart_settings import LocalScope

from .cleanup import cleanup
from .icons import icon_metadata_view
from .links import setup_metadata_type_list, setup_metadata_set_list

label = _(u'Metadata')
description = _(u'Handles document metadata.')
dependencies = ['app_registry', 'icons', 'navigation', 'documents', 'permissions', 'acls', 'common']
icon = icon_metadata_view

bootstrap_models = [
    {
        'name': 'metadatatype',
    },
    {
        'name': 'metadataset',
        'dependencies': ['metadata.metadatatype']
    },
    {
        'name': 'metadatasetitem',
        'dependencies': ['metadata.metadataset']
    },
    {
        'name': 'documenttypedefaults',
        'dependencies': ['documents.documenttype']
    },
]
cleanup_functions = [cleanup]


default_available_functions = {
    'current_date': datetime.datetime.now().date,
}

default_available_models = {
    'User': User
}

settings = [
    {
        'name': 'AVAILABLE_FUNCTIONS',
        'default': default_available_functions,
        'scopes': [LocalScope()]
    },
    {
        'name': 'AVAILABLE_MODELS',
        'default': default_available_models,
        'scopes': [LocalScope()]
    }
]
setup_links = [setup_metadata_type_list, setup_metadata_set_list]
