from __future__ import unicode_literals

import logging

from django.utils.module_loading import import_string

from .settings import GRAPHICS_BACKEND

logger = logging.getLogger(__name__)
backend = converter_class = import_string(GRAPHICS_BACKEND)
