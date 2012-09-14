from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from navigation.api import register_sidebar_template, bind_links
from navigation import Link
from documents.models import Document
from signaler.signals import post_update_index, pre_update_index

from .models import IndexableObject
from .links import search#, search_advanced, search_again

logger = logging.getLogger(__name__)


@receiver(pre_update_index, dispatch_uid='scheduler_shutdown_pre_update_index')
def scheduler_shutdown_pre_update_index(sender, mayan_runtime, **kwargs):
    logger.debug('Scheduler shut down on pre update index signal')
    logger.debug('Runtime variable: %s' % mayan_runtime)
    # Only shutdown the scheduler if the command is called from the command
    # line
    if not mayan_runtime:
        LocalScheduler.shutdown_all()


bind_links(['search', 'search_advanced', 'results'], [search], menu_name='form_header')
#bind_links(['results'], [search_again], menu_name='sidebar')

register_sidebar_template(['search'], 'search_help.html')
register_sidebar_template(['search'], 'recent_searches.html')

Document.add_to_class('mark_indexable', lambda obj: IndexableObject.objects.mark_indexable(obj))
