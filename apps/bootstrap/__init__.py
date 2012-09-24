from __future__ import absolute_import

from navigation.api import bind_links

from .links import (link_bootstrap_setup_create, link_bootstrap_setup_execute,
    link_bootstrap_setup_list, link_bootstrap_setup_edit, link_bootstrap_setup_delete,
    link_bootstrap_setup_view, link_bootstrap_setup_dump)
from .models import BootstrapSetup

bind_links([BootstrapSetup], [link_bootstrap_setup_view, link_bootstrap_setup_edit, link_bootstrap_setup_delete, link_bootstrap_setup_execute])
bind_links([BootstrapSetup], [link_bootstrap_setup_list, link_bootstrap_setup_create, link_bootstrap_setup_dump], menu_name='secondary_menu')
bind_links(['bootstrap_setup_list', 'bootstrap_setup_create', 'bootstrap_setup_dump'], [link_bootstrap_setup_list, link_bootstrap_setup_create, link_bootstrap_setup_dump], menu_name='secondary_menu')
