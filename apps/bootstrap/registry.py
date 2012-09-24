from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_bootstrap_setup
from .links import link_bootstrap_setup_tool, link_erase_database

label = _(u'Bootstrap')
description = _(u'Provides pre configured setups for indexes, document types, tags, etc.')
dependencies = ['app_registry', 'icons', 'navigation', 'documents', 'indexing', 'metadata', 'tags']
icon = icon_bootstrap_setup
setup_links = [link_bootstrap_setup_tool, link_erase_database]
