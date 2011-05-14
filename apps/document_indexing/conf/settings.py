"""Configuration options for the document_indexing app"""

import hashlib
import uuid

from django.utils.translation import ugettext_lazy as _

from common.utils import proper_name
from smart_settings.api import register_settings

available_indexing_functions = {
    'proper_name': proper_name
}

register_settings(
    namespace=u'document_indexing',
    module=u'document_indexing.conf.settings',
    settings=[
        # Definition
        {'name': u'AVAILABLE_INDEXING_FUNCTIONS', 'global_name': u'DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS', 'default': available_indexing_functions},
    ]
)
