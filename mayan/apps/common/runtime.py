from common.utils import load_backend

from .settings import SHARED_STORAGE

shared_storage_backend = load_backend(SHARED_STORAGE)()
