from __future__ import unicode_literals

from django.template import Library
from django.utils.importlib import import_module

register = Library()


@register.simple_tag
def app_version(app_name):
    try:
        app = import_module(app_name)
        return app.__version__
    except ImportError:
        return ''
