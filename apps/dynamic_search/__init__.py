from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from navigation.api import register_sidebar_template, register_links
from documents.models import Document
from scheduler.runtime import scheduler
from signaler.signals import post_update_index, pre_update_index

from .models import IndexableObject

logger = logging.getLogger(__name__)

search = {'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'}
#search_advanced = {'text': _(u'advanced search'), 'view': 'search_advanced', 'famfam': 'zoom_in'}
#search_again = {'text': _(u'search again'), 'view': 'search_again', 'famfam': 'arrow_undo'}

#register_sidebar_template(['search', 'search_advanced'], 'search_help.html')
register_sidebar_template(['search'], 'search_help.html')

#register_links(['search', 'search_advanced', 'results'], [search, search_advanced], menu_name='form_header')
register_links(['search'], [search], menu_name='form_header')
#register_links(['results'], [search_again], menu_name='sidebar')

#register_sidebar_template(['search', 'search_advanced', 'results'], 'recent_searches.html')
register_sidebar_template(['search'], 'recent_searches.html')

Document.add_to_class('mark_indexable', lambda obj: IndexableObject.objects.mark_indexable(obj))


@receiver(post_update_index, dispatch_uid='clear_pending_indexables')
def clear_pending_indexables(sender, **kwargs):
    logger.debug('Clearing all indexable flags post update index signal')
    IndexableObject.objects.clear_all()


@receiver(pre_update_index, dispatch_uid='scheduler_shutdown_pre_update_index')
def scheduler_shutdown_pre_update_index(sender, **kwargs):
    logger.debug('Scheduler shut down on pre update index signal')
    scheduler.shutdown()
