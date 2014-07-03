from __future__ import absolute_import

from common.utils import load_backend

from .conf.settings import STORAGE_BACKEND

storage_backend = load_backend(STORAGE_BACKEND)()
