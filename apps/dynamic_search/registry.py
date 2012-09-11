from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

#from .icons import icon_history_list
#from .links import history_list

label = _(u'Search')
#description = _(u'Handles the events registration and event logging.')
dependencies = ['app_registry', 'icons', 'navigation']
#icon = icon_history_list
#tool_links = [history_list]
#-    namespace=namespace,
#-    name='RECENT_COUNT',
#-    global_name='SEARCH_RECENT_COUNT',
#-    default=5,
#-    description=_(u'Maximum number of search queries to remember per user.')
#-)
#-
#-Setting(
#-    namespace=namespace,
#-    name='INDEX_UPDATE_INTERVAL',
#-    global_name='SEARCH_INDEX_UPDATE_INTERVAL',
#-    default=1800,
#-    description=_(u'Interval in second on which to trigger the search index update.')
