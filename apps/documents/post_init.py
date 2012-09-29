from __future__ import absolute_import

import tempfile

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.utils import validate_path

from .models import DocumentVersion, get_filename_from_uuid
from .settings import STORAGE_BACKEND, CACHE_PATH


#TODO: fix with method to set a settings value
if (validate_path(CACHE_PATH) == False) or (not CACHE_PATH):
    setattr(document_settings, 'CACHE_PATH', tempfile.mkdtemp())

DocumentVersion._meta.get_field('file').storage = STORAGE_BACKEND()
