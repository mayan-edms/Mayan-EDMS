from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_database_bootstrap
from .links import database_bootstrap, link_erase_database

label = _(u'Database bootstrap')
description = _(u'Provides pre configured setups for indexes, document types, tags.')
dependencies = ['app_registry', 'icons', 'navigation', 'documents', 'indexing', 'metadata', 'tags']
icon = icon_database_bootstrap
setup_links = [database_bootstrap, link_erase_database]
