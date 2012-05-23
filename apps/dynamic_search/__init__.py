from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from django.core.management import call_command

from navigation.api import register_sidebar_template, bind_links, Link
from documents.models import Document
from scheduler.runtime import scheduler
from signaler.signals import post_update_index, pre_update_index
from scheduler.api import register_interval_job
from lock_manager import Lock, LockError

from .models import IndexableObject
from .conf.settings import INDEX_UPDATE_INTERVAL

logger = logging.getLogger(__name__)

search = Link(text=_(u'search'), view='search', sprite='zoom')
search_advanced = Link(text=_(u'advanced search'), view='search_advanced', sprite='zoom_in')
search_again = Link(text=_(u'search again'), view='search_again', sprite='arrow_undo')

register_sidebar_template(['search'], 'search_help.html')

register_links(['search'], [search], menu_name='form_header')

register_sidebar_template(['search'], 'recent_searches.html')

Document.add_to_class('mark_indexable', lambda obj: IndexableObject.objects.mark_indexable(obj))


@receiver(pre_update_index, dispatch_uid='scheduler_shutdown_pre_update_index')
def scheduler_shutdown_pre_update_index(sender, mayan_runtime, **kwargs):
    logger.debug('Scheduler shut down on pre update index signal')
    logger.debug('Runtime variable: %s' % mayan_runtime)
    # Only shutdown the scheduler if the command is called from the command
    # line
    if not mayan_runtime:
        scheduler.shutdown()


def search_index_update():
    lock_id = u'search_index_update'
    try:
        logger.debug('trying to acquire lock: %s' % lock_id)
        lock = Lock.acquire_lock(lock_id)
        logger.debug('acquired lock: %s' % lock_id)

        logger.debug('Executing haystack\'s index update command')
        call_command('update_index', '--mayan_runtime')

        lock.release()
    except LockError:
        logger.debug('unable to obtain lock')
        pass
    except Exception, instance:
        logger.debug('Unhandled exception: %s' % instance)
        lock.release()
        pass

bind_links(['search', 'search_advanced', 'results'], [search, search_advanced], menu_name='form_header')
bind_links(['results'], [search_again], menu_name='sidebar')

register_interval_job('search_index_update', _(u'Update the search index with the most recent modified documents.'), search_index_update, seconds=INDEX_UPDATE_INTERVAL)
