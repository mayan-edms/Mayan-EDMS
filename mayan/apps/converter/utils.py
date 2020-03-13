from __future__ import unicode_literals

import logging

from django.utils.module_loading import import_string

from .settings import setting_graphics_backend

logger = logging.getLogger(name=__name__)


def get_converter_class():
    return import_string(dotted_path=setting_graphics_backend.value)
