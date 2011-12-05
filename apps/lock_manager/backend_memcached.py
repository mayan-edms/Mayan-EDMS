from django.core.cache import get_cache

if CACHE_URI:
    try:
        cache_backend = get_cache(CACHE_URI)
    except ImportError:
        # TODO: display or log error
        cache_backend = None
else:
    cache_backend = None
if cache_backend:
    acquire_lock = lambda lock_id: cache_backend.add(lock_id, u'true', LOCK_EXPIRE)
    release_lock = lambda lock_id: cache_backend.delete(lock_id)
else:
    acquire_lock = lambda lock_id: True
    release_lock = lambda lock_id: True
