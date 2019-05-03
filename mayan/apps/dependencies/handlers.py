from __future__ import unicode_literals

from .classes import JavaScriptDependency


def handler_install_javascript(sender, **kwargs):
    JavaScriptDependency.install_multiple(subclass_only=True)
