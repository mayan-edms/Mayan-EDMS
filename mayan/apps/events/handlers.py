from __future__ import unicode_literals

from .utils import create_system_user


def handler_create_system_user(sender, **kwargs):
    create_system_user()
