from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common.apps import MayanAppConfig


class OrganizationApp(MayanAppConfig):
    name = 'organizations'
    verbose_name = _('Organizations')
