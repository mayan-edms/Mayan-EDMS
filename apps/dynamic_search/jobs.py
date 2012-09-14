import logging

from django.core.management import call_command

from lock_manager import Lock, LockError

logger = logging.getLogger(__name__)


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
