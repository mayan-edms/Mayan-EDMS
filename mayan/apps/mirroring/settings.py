from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_MIRRORING_DOCUMENT_CACHE_LOOKUP_TIMEOUT,
    DEFAULT_MIRRORING_NODE_CACHE_LOOKUP_TIMEOUT
)

namespace = SettingNamespace(label=_('Mirroring'), name='mirroring')

setting_document_lookup_cache_timeout = namespace.add_setting(
    default=DEFAULT_MIRRORING_DOCUMENT_CACHE_LOOKUP_TIMEOUT,
    global_name='MIRRORING_DOCUMENT_CACHE_LOOKUP_TIMEOUT',
    help_text=_('Time in seconds to cache the path lookup to a document.')
)
setting_node_lookup_cache_timeout = namespace.add_setting(
    default=DEFAULT_MIRRORING_NODE_CACHE_LOOKUP_TIMEOUT,
    global_name='MIRRORING_NODE_CACHE_LOOKUP_TIMEOUT',
    help_text=_('Time in seconds to cache the path lookup to an index node.')
)
