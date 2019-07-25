from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('File caching'), name='file_caching')

permission_cache_purge = namespace.add_permission(
    label=_('Purge a file cache'), name='file_caching_cache_purge'
)
permission_cache_view = namespace.add_permission(
    label=_('View a file cache'), name='file_caching_cache_view'
)
