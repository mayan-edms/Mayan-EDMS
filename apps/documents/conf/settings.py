"""Configuration options for the documents app"""

import hashlib
import uuid
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from storage.backends.filebasedstorage import FileBasedStorage
from smart_settings.api import Setting, SettingNamespace

def default_checksum(x):
    """hashlib.sha256(x).hexdigest()"""
    return hashlib.sha256(x).hexdigest()


def default_uuid():
    """unicode(uuid.uuid4())"""
    return unicode(uuid.uuid4())


namespace = SettingNamespace('documents', _(u'Documents'), module='documents.conf.settings')

# Saving

Setting(
    namespace=namespace,
    name='CHECKSUM_FUNCTION',
    global_name='DOCUMENTS_CHECKSUM_FUNCTION',
    default=default_checksum,
)

Setting(
    namespace=namespace,
    name='UUID_FUNCTION',
    global_name='DOCUMENTS_UUID_FUNCTION',
    default=default_uuid,
)

# Storage

Setting(
    namespace=namespace,
    name='STORAGE_BACKEND',
    global_name='DOCUMENTS_STORAGE_BACKEND',
    default=FileBasedStorage,
)

# Usage

Setting(
    namespace=namespace,
    name='PREVIEW_SIZE',
    global_name='DOCUMENTS_PREVIEW_SIZE',
    default=u'640x480',
)

Setting(
    namespace=namespace,
    name='PRINT_SIZE',
    global_name='DOCUMENTS_PRINT_SIZE',
    default=u'1400',
)

Setting(
    namespace=namespace,
    name='MULTIPAGE_PREVIEW_SIZE',
    global_name='DOCUMENTS_MULTIPAGE_PREVIEW_SIZE',
    default=u'160x120',
)

Setting(
    namespace=namespace,
    name='THUMBNAIL_SIZE',
    global_name='DOCUMENTS_THUMBNAIL_SIZE',
    default=u'50x50',
)

Setting(
    namespace=namespace,
    name='DISPLAY_SIZE',
    global_name='DOCUMENTS_DISPLAY_SIZE',
    default=u'1200',
)

Setting(
    namespace=namespace,
    name='RECENT_COUNT',
    global_name='DOCUMENTS_RECENT_COUNT',
    default=40,
    description=_(u'Maximum number of recent (created, edited, viewed) documents to remember per user.'),
)

Setting(
    namespace=namespace,
    name='ZOOM_PERCENT_STEP',
    global_name='DOCUMENTS_ZOOM_PERCENT_STEP',
    default=50,
    description=_(u'Amount in percent zoom in or out a document page per user interaction.'),
)

Setting(
    namespace=namespace,
    name='ZOOM_MAX_LEVEL',
    global_name='DOCUMENTS_ZOOM_MAX_LEVEL',
    default=200,
    description=_(u'Maximum amount in percent (%) to allow user to zoom in a document page interactively.'),
)

Setting(
    namespace=namespace,
    name='ZOOM_MIN_LEVEL',
    global_name='DOCUMENTS_ZOOM_MIN_LEVEL',
    default=50,
    description=_(u'Minimum amount in percent (%) to allow user to zoom out a document page interactively.'),
)

Setting(
    namespace=namespace,
    name='ROTATION_STEP',
    global_name='DOCUMENTS_ROTATION_STEP',
    default=90,
    description=_(u'Amount in degrees to rotate a document page per user interaction.'),
)

Setting(
    namespace=namespace,
    name='CACHE_PATH',
    global_name='DOCUMENTS_CACHE_PATH',
    default=os.path.join(settings.PROJECT_ROOT, 'image_cache'),
    exists=True
)
