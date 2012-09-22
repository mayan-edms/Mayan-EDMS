from __future__ import absolute_import

import tempfile

from .utils import validate_path
import common.settings as common_settings


def init_validate_temp_path():
    if (validate_path(common_settings.TEMPORARY_DIRECTORY) == False) or (not common_settings.TEMPORARY_DIRECTORY):
        setattr(common_settings, 'TEMPORARY_DIRECTORY', tempfile.mkdtemp())
