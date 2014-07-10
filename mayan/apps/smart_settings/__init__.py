from __future__ import absolute_import

from project_setup.api import register_setup

from .links import check_settings

register_setup(check_settings)
