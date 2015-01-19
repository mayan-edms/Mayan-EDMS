from common.utils import load_backend

from .settings import STORAGE_BACKEND

storage_backend = load_backend(STORAGE_BACKEND)()
