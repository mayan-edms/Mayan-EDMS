from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace


namespace = Namespace(name='dynamic_search', label=_('Search'))
SHOW_OBJECT_TYPE = namespace.add_setting(global_name='SEARCH_SHOW_OBJECT_TYPE', default=True)
LIMIT = namespace.add_setting(global_name='SEARCH_LIMIT', default=100, help_text=_('Maximum amount search hits to fetch and display.'))
RECENT_COUNT = namespace.add_setting(global_name='SEARCH_RECENT_COUNT', default=5, help_text=_('Maximum number of search queries to remember per user.'))
