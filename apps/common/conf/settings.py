from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from common.literals import PAGE_SIZE_LETTER, PAGE_ORIENTATION_PORTRAIT

TEMPORARY_DIRECTORY = getattr(settings, 'COMMON_TEMPORARY_DIRECTORY', u'/tmp')

setting_description = {
    'COMMON_TEMPORARY_DIRECTORY': _(u'Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp()')
}

# Printing
DEFAULT_PAPER_SIZE = getattr(settings, 'COMMON_DEFAULT_PAPER_SIZE', PAGE_SIZE_LETTER)
DEFAULT_PAGE_ORIENTATION = getattr(settings, 'COMMON_DEFAULT_PAGE_ORIENTATION', PAGE_ORIENTATION_PORTRAIT)
