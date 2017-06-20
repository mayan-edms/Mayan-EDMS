from __future__ import unicode_literals

from django.apps import apps

from .base import LockingBackend


class ModelLock(LockingBackend):
    @classmethod
    def acquire_lock(cls, name, timeout=None):
        Lock = apps.get_model(app_label='lock_manager', model_name='Lock')
        return Lock.objects.acquire_lock(name=name, timeout=timeout)

    @classmethod
    def purge_locks(cls):
        Lock = apps.get_model(app_label='lock_manager', model_name='Lock')
        Lock.objects.select_for_update().delete()
