from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from project_setup.api import register_setup

from .links import check_settings

register_setup(check_settings)
