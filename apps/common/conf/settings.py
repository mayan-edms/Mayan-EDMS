from django.conf import settings
from django.utils.translation import ugettext_lazy as _

TEMPORARY_DIRECTORY = getattr(settings, 'COMMON_TEMPORARY_DIRECTORY', u'/tmp')

setting_description = {
    'COMMON_TEMPORARY_DIRECTORY': _(u'Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp()')
}
