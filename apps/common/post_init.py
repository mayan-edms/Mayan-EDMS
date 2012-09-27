from __future__ import absolute_import

import tempfile

from .utils import validate_path
import common.settings as common_settings

from .settings import TEMPORARY_DIRECTORY

if (validate_path(getattr(common_settings, 'TEMPORARY_DIRECTORY')) == False) or (not getattr(common_settings, 'TEMPORARY_DIRECTORY')):
    setattr(common_settings, 'TEMPORARY_DIRECTORY', tempfile.mkdtemp())
