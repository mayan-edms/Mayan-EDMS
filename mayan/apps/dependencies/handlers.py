from __future__ import unicode_literals

from .javascript import JSDependencyManager


def handler_install_javascript(sender, **kwargs):
    js_manager = JSDependencyManager()
    js_manager.install()
