from __future__ import unicode_literals

from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _

from common.apps import MayanAppConfig


class OrganizationApp(AppConfig):
    name = 'organizations'
    verbose_name = _('Organizations')
