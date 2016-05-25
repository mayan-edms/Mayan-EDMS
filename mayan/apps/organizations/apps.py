from __future__ import unicode_literals

from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _

from common.apps import MayanAppConfig

from .utils import create_default_organization


class OrganizationApp(AppConfig):
    name = 'organizations'
    verbose_name = _('Organizations')

    def ready(self):
        super(OrganizationApp, self).ready()
        Organization = self.get_model('Organization')
        create_default_organization(verbosity=0)
