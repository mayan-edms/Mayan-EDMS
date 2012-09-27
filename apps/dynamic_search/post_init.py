from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from scheduler.api import LocalScheduler

from .settings import INDEX_UPDATE_INTERVAL
from .jobs import search_index_update


dynamic_search_scheduler = LocalScheduler('search', _(u'Search'))
dynamic_search_scheduler.add_interval_job('search_index_update', _(u'Update the search index with the most recent modified documents.'), search_index_update, seconds=INDEX_UPDATE_INTERVAL)
dynamic_search_scheduler.start()
