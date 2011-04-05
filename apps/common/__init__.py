import tempfile

from common.conf import settings as common_settings

TEMPORARY_DIRECTORY = common_settings.TEMPORARY_DIRECTORY \
    if common_settings.TEMPORARY_DIRECTORY else tempfile.mkdtemp()
