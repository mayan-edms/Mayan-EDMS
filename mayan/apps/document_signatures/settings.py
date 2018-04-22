from __future__ import unicode_literals

import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='signatures', label=_('Document signatures'))
setting_storage_backend = namespace.add_setting(
    global_name='SIGNATURES_STORAGE_BACKEND',
    default='django.core.files.storage.FileSystemStorage'
)
setting_storage_backend_arguments = namespace.add_setting(
    global_name='SIGNATURES_STORAGE_BACKEND_ARGUMENTS',
    default='{{location: {}}}'.format(
        os.path.join(settings.MEDIA_ROOT, 'document_signatures')
    )
)
