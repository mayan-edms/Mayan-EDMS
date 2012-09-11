from __future__ import absolute_import

from django.core.exceptions import ImproperlyConfigured

from .office_converter import OfficeConverter
from .exceptions import OfficeBackendError
from .settings import GRAPHICS_BACKEND
from .utils import load_backend

try:
    office_converter = OfficeConverter()
except OfficeBackendError:
    office_converter = None

try:
    backend = load_backend().ConverterClass()
except ImproperlyConfigured:
    raise ImproperlyConfigured(u'Missing or incorrect converter backend: %s' % GRAPHICS_BACKEND)
