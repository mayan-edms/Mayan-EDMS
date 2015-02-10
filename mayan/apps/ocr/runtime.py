from common.utils import load_backend

from .settings import BACKEND

ocr_backend = load_backend(BACKEND)()
