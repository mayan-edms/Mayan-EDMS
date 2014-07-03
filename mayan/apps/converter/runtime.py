from __future__ import absolute_import

from common.utils import load_backend

from .conf.settings import GRAPHICS_BACKEND
from .exceptions import OfficeBackendError
from .office_converter import OfficeConverter

try:
    office_converter = OfficeConverter()
except OfficeBackendError:
    office_converter = None

backend = load_backend(GRAPHICS_BACKEND)()
