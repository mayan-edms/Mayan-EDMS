from __future__ import absolute_import

from project_setup.api import register_setup

from .classes import SettingsNamespace, LocalScope
from .links import link_settings

register_setup(link_settings)
