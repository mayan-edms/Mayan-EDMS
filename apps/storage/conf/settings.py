"""Configuration options for the storage app"""
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('storage', _(u'Storage'), module='storage.conf.settings')

Setting(
    namespace=namespace,
    name='GRIDFS_HOST',
    global_name='STORAGE_GRIDFS_HOST',
    default=u'localhost',
)

Setting(
    namespace=namespace,
    name='GRIDFS_PORT',
    global_name='STORAGE_GRIDFS_PORT',
    default=27017,
)

Setting(
    namespace=namespace,
    name='GRIDFS_DATABASE_NAME',
    global_name='STORAGE_GRIDFS_DATABASE_NAME',
    default='document_storage',
)

Setting(
    namespace=namespace,
    name='FILESTORAGE_LOCATION',
    global_name='STORAGE_FILESTORAGE_LOCATION',
    default=os.path.join(settings.PROJECT_ROOT, u'document_storage'),
    exists=True
)
