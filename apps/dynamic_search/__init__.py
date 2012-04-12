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

register_sidebar_template(['search'], 'search_help.html')

register_links(['search'], [search], menu_name='form_header')

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
