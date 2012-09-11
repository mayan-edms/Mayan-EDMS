from __future__ import absolute_import

import tempfile

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.utils import validate_path, encapsulate

from .models import DocumentVersion, get_filename_from_uuid
from .settings import STORAGE_BACKEND, CACHE_PATH


def init_validate_cache_path():
    if (validate_path(CACHE_PATH) == False) or (not CACHE_PATH):
        setattr(document_settings, 'CACHE_PATH', tempfile.mkdtemp())

def init_set_storage_backend():
    DocumentVersion._meta.get_field('file').storage=STORAGE_BACKEND()
