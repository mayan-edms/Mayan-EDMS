"""
Configuration options for the documents app
"""
from __future__ import absolute_import

import hashlib
import uuid
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from storage.backends.filebasedstorage import FileBasedStorage
from smart_settings import LocalScope

from .icons import icon_documents
from .links import document_type_setup
from .statistics import get_statistics
from .cleanup import cleanup

def default_checksum(x):
    """hashlib.sha256(x).hexdigest()"""
    return hashlib.sha256(x).hexdigest()


def default_uuid():
    """unicode(uuid.uuid4())"""
    return unicode(uuid.uuid4())


label = _(u'Documents')
description = _(u'Base app that handles documents instances.')
icon = icon_documents
dependencies = ['app_registry', 'icons', 'storage', 'permissions', 'navigation']
setup_links = [document_type_setup]
bootstrap_models = [
    {
        'name': 'documenttype',
    },
    {
        'name': 'documenttypefilename',
        'dependencies': ['documents.documenttype']
    }
]
cleanup_functions = [cleanup]
settings = [
    {
        'name': 'IM_CONVERT_PATH',
        'default': u'/usr/bin/convert',
        'description': _(u'File path to imagemagick\'s convert program.'),
        'exists': True,
        'scopes': [LocalScope()]
    },

# Saving

    {
        'name': 'CHECKSUM_FUNCTION',
        'default': default_checksum,
        'scopes': [LocalScope()]
    },
    {
        'name': 'UUID_FUNCTION',
        'default': default_uuid,
        'scopes': [LocalScope()]
    },

# Storage

    {
        'name': 'STORAGE_BACKEND',
        'default': FileBasedStorage,
        'scopes': [LocalScope()]
    },

# Usage

    {
        'name': 'PREVIEW_SIZE',
        'default': u'640x480',
        'scopes': [LocalScope()]
    },
    {
        'name': 'PRINT_SIZE',
        'default': u'1400',
        'scopes': [LocalScope()]
    },
    {
        'name': 'MULTIPAGE_PREVIEW_SIZE',
        'default': u'160x120',
        'scopes': [LocalScope()]
    },
    {
        'name': 'THUMBNAIL_SIZE',
        'default': u'50x50',
        'scopes': [LocalScope()]
    },
    {
        'name': 'DISPLAY_SIZE',
        'default': u'1200',
        'scopes': [LocalScope()]
    },
    {
        'name': 'RECENT_COUNT',
        'default': 40,
        'description': _(u'Maximum number of recent (created, edited, viewed}, documents to remember per user.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'ZOOM_PERCENT_STEP',
        'default': 50,
        'description': _(u'Amount in percent zoom in or out a document page per user interaction.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'ZOOM_MAX_LEVEL',
        'default': 200,
        'description': _(u'Maximum amount in percent (%}, to allow user to zoom in a document page interactively.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'ZOOM_MIN_LEVEL',
        'default': 50,
        'description': _(u'Minimum amount in percent (%}, to allow user to zoom out a document page interactively.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'ROTATION_STEP',
        'default': 90,
        'description': _(u'Amount in degrees to rotate a document page per user interaction.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'CACHE_PATH',
        'default': os.path.join(django_settings.PROJECT_ROOT, 'image_cache'),
        'exists': True,
        'scopes': [LocalScope()]
    },
]
statistics=[get_statistics]
