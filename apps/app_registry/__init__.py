from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from .models import App


def register_apps():
    for app_name in settings.INSTALLED_APPS:
        App.register(app_name)
        try:
            post_init = import_module('%s.post_init' % app_name)
        except ImportError as exception:
            pass


register_apps()
