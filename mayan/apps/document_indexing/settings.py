from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

available_indexing_functions = {
}

namespace = Namespace(name='document_indexing', label=_('Indexing'))
setting_available_indexing_functions = namespace.add_setting(
    global_name='DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS',
    default=available_indexing_functions
)
