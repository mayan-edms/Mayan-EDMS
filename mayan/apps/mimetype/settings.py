from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings import Namespace

from .literals import DEFAULT_MIMETYPE_FILE_READ_SIZE

namespace = Namespace(label=_('MIME type'), name='mimetype')

setting_file_read_size = namespace.add_setting(
    default=DEFAULT_MIMETYPE_FILE_READ_SIZE,
    global_name='MIMETYPE_FILE_READ_SIZE', help_text=_(
        'Amount of bytes to read from a document to determine its MIME type. '
        'Setting it to 0 disables the feature and attempts to read the entire '
        'document file into memory.'
    )
)
