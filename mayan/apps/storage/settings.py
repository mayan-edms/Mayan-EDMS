from __future__ import unicode_literals

import tempfile

from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

namespace = Namespace(label=_('Storage'), name='storage')

setting_temporary_directory = namespace.add_setting(
    global_name='STORAGE_TEMPORARY_DIRECTORY', default=tempfile.gettempdir(),
    help_text=_(
        'Temporary directory used site wide to store thumbnails, previews '
        'and temporary files.'
    )
)
