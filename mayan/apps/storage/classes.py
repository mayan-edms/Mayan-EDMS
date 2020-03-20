from __future__ import unicode_literals

import logging

from django.core.files.storage import Storage
from django.utils.module_loading import import_string

from .literals import DEFAULT_STORAGE_BACKEND

logger = logging.getLogger(name=__name__)


class FakeStorageSubclass(object):
    """
    Placeholder class to allow serializing the real storage subclass to
    support migrations.
    """
    def __eq__(self, other):
        return True


class PassthroughStorage(Storage):
    def __init__(self, *args, **kwargs):
        logger.debug(
            'initializing passthrought storage with: %s, %s', args, kwargs
        )
        storage_backend = kwargs.pop(
            'storage_backend', DEFAULT_STORAGE_BACKEND
        )
        storage_backend_arguments = kwargs.pop(
            'storage_backend_arguments', {}
        )
        self.upstream_storage_backend = import_string(
            dotted_path=storage_backend
        )(
            **storage_backend_arguments
        )
        super(PassthroughStorage, self).__init__(*args, **kwargs)

    def _call_backend_method(self, method_name, kwargs):
        return getattr(self.upstream_storage_backend, method_name)(**kwargs)

    def exists(self, *args, **kwargs):
        return self.upstream_storage_backend.exists(*args, **kwargs)
