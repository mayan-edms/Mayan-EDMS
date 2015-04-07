from __future__ import unicode_literals

import logging

from django.utils.module_loading import import_string

from .exceptions import OfficeBackendError
from .office_converter import OfficeConverter
from .settings import GRAPHICS_BACKEND

logger = logging.getLogger(__name__)

logger.debug('initializing office backend')
try:
    office_converter = OfficeConverter()
except OfficeBackendError as exception:
    logger.error('error initializing office backend; %s', exception)
    office_converter = None
else:
    logger.debug('office_backend initialized')


backend = import_string(GRAPHICS_BACKEND)()
