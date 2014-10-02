from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from navigation.api import register_top_menu
from project_setup.api import register_setup
from project_tools.api import register_tool

from .links import admin_site, diagnostics, maintenance_menu, sentry
from .settings import DISABLE_HOME_VIEW

if not DISABLE_HOME_VIEW:
    register_top_menu('home', link={'text': _(u'Home'), 'view': 'main:home', 'famfam': 'house'}, position=0)

if 'django.contrib.admin' in django_settings.INSTALLED_APPS:
    register_setup(admin_site)

register_tool(diagnostics)
register_tool(maintenance_menu)

# TODO: Remove this
if 'sentry' in django_settings.INSTALLED_APPS:
    register_tool(sentry)
