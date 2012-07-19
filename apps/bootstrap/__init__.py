from __future__ import absolute_import

from project_setup.api import register_setup
from navigation.api import register_links#, register_sidebar_template
    
from .links import database_bootstrap, bootstrap_execute
from .api import BootstrapSimple

register_setup(database_bootstrap)
register_links(BootstrapSimple, [bootstrap_execute])
