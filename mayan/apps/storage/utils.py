from __future__ import unicode_literals

import logging
import os
import shutil
import tempfile

from django.utils.module_loading import import_string

from .settings import setting_temporary_directory

logger = logging.getLogger(__name__)


def TemporaryFile(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.TemporaryFile(*args, **kwargs)


def NamedTemporaryFile(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.NamedTemporaryFile(*args, **kwargs)


def fs_cleanup(filename, file_descriptor=None, suppress_exceptions=True):
    """
    Tries to remove the given filename. Ignores non-existent files
    """
    if file_descriptor:
        os.close(file_descriptor)

    try:
        os.remove(filename)
    except OSError:
        try:
            shutil.rmtree(filename)
        except OSError:
            if suppress_exceptions:
                pass
            else:
                raise


def get_storage_subclass(dotted_path):
    """
    Import a storage class and return a subclass that will always return eq
    True to avoid creating a new migration when for runtime storage class
    changes.
    """
    imported_storage_class = import_string(dotted_path=dotted_path)

    class StorageSubclass(imported_storage_class):
        def __init__(self, *args, **kwargs):
            return super(StorageSubclass, self).__init__(*args, **kwargs)

        def __eq__(self, other):
            return True

        def deconstruct(self):
            return ('mayan.apps.storage.classes.FakeStorageSubclass', (), {})

    return StorageSubclass


def mkdtemp(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.mkdtemp(*args, **kwargs)


def mkstemp(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.mkstemp(*args, **kwargs)


def validate_path(path):
    if not os.path.exists(path):
        # If doesn't exist try to create it
        try:
            os.mkdir(path)
        except Exception as exception:
            logger.debug('unhandled exception: %s', exception)
            return False

    # Check if it is writable
    try:
        fd, test_filepath = tempfile.mkstemp(dir=path)
        os.close(fd)
        os.unlink(test_filepath)
    except Exception as exception:
        logger.debug('unhandled exception: %s', exception)
        return False

    return True
