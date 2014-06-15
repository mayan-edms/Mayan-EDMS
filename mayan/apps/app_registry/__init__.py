from __future__ import absolute_import

import logging

from django.conf import settings
from django.utils.importlib import import_module

from .models import App

logger = logging.getLogger(__name__)


def register_apps():
    for app_name in settings.INSTALLED_APPS:
        logger.debug('registering: %s' % app_name)
        App.register(app_name)
        try:
            post_init = import_module('%s.post_init' % app_name)
        except ImportError:
            logger.debug('Unable to import post_init module from: %s' % app_name)


register_apps()
