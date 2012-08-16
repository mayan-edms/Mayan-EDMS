from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from app_registry import register_app, UnableToRegister
from navigation.api import bind_links
from project_setup.api import register_setup

from .links import database_bootstrap, bootstrap_execute, erase_database_link
from .api import BootstrapSimple, BootstrapPermit

register_setup(database_bootstrap)
register_setup(erase_database_link)
bind_links([BootstrapSimple], [bootstrap_execute])
bind_links([BootstrapPermit], [bootstrap_execute])

try:
    register_app('bootstrap', _(u'Database bootstrap'))
except UnableToRegister:
    pass
