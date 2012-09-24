from __future__ import absolute_import

import inspect

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from .models import App


def register_apps():
    for app_name in settings.INSTALLED_APPS:
        App.register(app_name)
        try:
            post_init = import_module('%s.post_init' % app_name)
        except ImportError:
            pass
        else:
            if post_init:
                for name, value in inspect.getmembers(post_init):
                    if hasattr(value, '__call__') and name.startswith('init'):
                        value()


register_apps()
