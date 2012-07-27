from __future__ import absolute_import

from project_setup.api import register_setup
from navigation.api import bind_links

from .links import database_bootstrap, bootstrap_execute, erase_database_link
from .api import BootstrapSimple, BootstrapPermit

register_setup(database_bootstrap)
register_setup(erase_database_link)
bind_links([BootstrapSimple], [bootstrap_execute])
bind_links([BootstrapPermit], [bootstrap_execute])
