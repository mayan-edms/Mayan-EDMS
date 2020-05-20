import logging

from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.module_loading import import_string
from django.utils.six import BytesIO, StringIO, raise_from
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.class_mixins import ModuleLoaderMixin

from .literals import DEFAULT_STORAGE_BACKEND

logger = logging.getLogger(name=__name__)


class BufferedFile(File):
    def __init__(self, file_object, mode, name=None):
        self.file_object = file_object
        self.mode = mode
        if 'b' in mode:
            self.stream = BytesIO()
        else:
            self.stream = StringIO()

        self.stream_size = 0

    def close(self):
        self.file_object.close()
        self.stream.close()

    def read(self, size=None):
        if size is None:
            size = -1

        if size == -1 or size > self.stream_size:
            while True:
                position = self.stream.tell()
                chunk = self._get_file_object_chunk()
                if chunk:
                    self.stream_size += len(chunk)
                    self.stream.write(chunk)
                    self.stream.seek(position)
                    if self.stream_size >= size and size != -1:
                        break
                else:
                    break

        if size:
            read_size = min(size, self.stream_size)
            self.stream_size -= read_size
        else:
            read_size = None

        return self.stream.read(read_size)


class DefinedStorage(ModuleLoaderMixin, object):
    _loader_module_name = 'storages'
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, dotted_path, label, name, kwargs, error_message=None):
        self.dotted_path = dotted_path
        self.error_message = error_message
        self.label = label
        self.name = name
        self.kwargs = kwargs or {}
        self.__class__._registry[name] = self

    def __eq__(self, other):
        return True

    def get_storage_instance(self):
        try:
            return self.get_storage_subclass()(**self.kwargs)
        except Exception as exception:
            message = self.error_message or _(
                'Unable to initialize storage: %(name)s. Check the storage '
                'backend dotted path and arguments.'
            ) % {
                'name': self.name
            }

            logger.fatal(message)
            raise_from(value=TypeError(message), from_value=exception)

    def get_storage_subclass(self):
        """
        Import a storage class and return a subclass that will always return eq
        True to avoid creating a new migration when for runtime storage class
        changes.
        """
        try:
            imported_storage_class = import_string(
                dotted_path=self.dotted_path
            )
        except Exception as exception:
            message = self.error_message or _(
                'Unable to initialize storage: %(name)s. Check the storage '
                'backend dotted path and arguments.'
            ) % {
                'name': self.name
            }

            logger.fatal(message)
            raise_from(value=TypeError(message), from_value=exception)

        class DynamicStorageSubclass(imported_storage_class):
            def __init__(self, *args, **kwargs):
                return super(DynamicStorageSubclass, self).__init__(
                    *args, **kwargs
                )

            def __eq__(self, other):
                return True

            def deconstruct(self):
                return (
                    'mayan.apps.storage.classes.FakeStorageSubclass', (), {}
                )

        return DynamicStorageSubclass


def defined_storage_proxy_method(method_name):
    def inner_function(self, *args, **kwargs):
        return getattr(
            DefinedStorage.get(name=self.name).get_storage_instance(), method_name
        )(*args, **kwargs)

    return inner_function


class DefinedStorageLazy(object):
    def __init__(self, name):
        self.name = name
        super(DefinedStorageLazy, self).__init__()

    delete = defined_storage_proxy_method(method_name='delete')
    exists = defined_storage_proxy_method(method_name='exists')
    generate_filename = defined_storage_proxy_method(
        method_name='generate_filename'
    )
    open = defined_storage_proxy_method(method_name='open')
    path = defined_storage_proxy_method(method_name='path')
    save = defined_storage_proxy_method(method_name='save')
    size = defined_storage_proxy_method(method_name='size')


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
        next_storage_backend = kwargs.pop(
            'next_storage_backend', DEFAULT_STORAGE_BACKEND
        )
        next_storage_backend_arguments = kwargs.pop(
            'next_storage_backend_arguments', {}
        )

        self.next_storage_class = import_string(
            dotted_path=next_storage_backend
        )

        self.next_storage_backend = self.next_storage_class(
            **next_storage_backend_arguments
        )
        super(PassthroughStorage, self).__init__(*args, **kwargs)

    def _call_backend_method(self, method_name, kwargs):
        return getattr(self.next_storage_backend, method_name)(**kwargs)

    def delete(self, *args, **kwargs):
        return self.next_storage_backend.delete(*args, **kwargs)

    def exists(self, *args, **kwargs):
        return self.next_storage_backend.exists(*args, **kwargs)

    def path(self, *args, **kwargs):
        return self.next_storage_backend.path(*args, **kwargs)

    def size(self, *args, **kwargs):
        return self.next_storage_backend.size(*args, **kwargs)
