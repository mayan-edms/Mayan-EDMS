from __future__ import unicode_literals

import logging

from django import apps
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig

#from .links import (
#    link_about, link_current_user_details, link_current_user_edit,
#    link_current_user_locale_profile_details,
#    link_current_user_locale_profile_edit, link_filters, link_license,
#    link_packages_licenses, link_setup, link_tools
#)

logger = logging.getLogger(__name__)


class MOTDApp(MayanAppConfig):
    name = 'motd'
    test = True
    verbose_name = _('Message of the day')

    def ready(self):
        super(MOTDApp, self).ready()
