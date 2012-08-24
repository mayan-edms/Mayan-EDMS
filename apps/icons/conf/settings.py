"""
Configuration options for the documents app
"""
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from storage.backends.filebasedstorage import FileBasedStorage
from smart_settings.api import Setting, SettingNamespace
from ..literals import DEFAULT_ICON_SET

from .. import app
print '__file__', __file__
namespace = SettingNamespace(app.name, app.label, module='icons.conf.settings', sprite='page')

# Saving

Setting(
    namespace=namespace,
    name='ICON_SET',
    global_name='ICONS_ICON_SET',
    default=DEFAULT_ICON_SET,
)
