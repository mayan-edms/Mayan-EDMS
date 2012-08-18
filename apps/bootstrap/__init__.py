from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links
from project_setup.api import register_setup
from app_registry.models import App

from .links import database_bootstrap, bootstrap_execute, erase_database_link
from .api import BootstrapSimple, BootstrapPermit

register_setup(database_bootstrap)
register_setup(erase_database_link)
bind_links([BootstrapSimple], [bootstrap_execute])
bind_links([BootstrapPermit], [bootstrap_execute])

try:
    app = App.register('bootstrap', _(u'Database bootstrap'))
except App.UnableToRegister:
    pass
else:
    app.set_dependencies(['app_registry'])
