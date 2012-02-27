from __future__ import absolute_import

from .office_converter import OfficeConverter
from .exceptions import OfficeBackendError


try:
    office_converter = OfficeConverter()
except OfficeBackendError:
    office_converter = None
