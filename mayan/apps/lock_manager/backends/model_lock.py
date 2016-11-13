from __future__ import unicode_literals

from django.apps import apps


class ModelLock(object):
    @classmethod
    def acquire_lock(cls, name, timeout=None):
        Lock = apps.get_model(app_label='lock_manager', model_name='Lock')
        return Lock.objects.acquire_lock(name=name, timeout=timeout)
