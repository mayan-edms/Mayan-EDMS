import dbm
import logging
import os
from pathlib import Path
import shutil
import tempfile

from django.apps import apps
from django.utils.module_loading import import_string

from .classes import DefinedStorage, PassthroughStorage
from .settings import setting_temporary_directory

logger = logging.getLogger(name=__name__)


def NamedTemporaryFile(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.NamedTemporaryFile(*args, **kwargs)


class PassthroughStorageProcessor(object):
    def __init__(
        self, app_label, defined_storage_name, log_file, model_name,
        file_attribute='file'
    ):
        self.app_label = app_label
        self.defined_storage_name = defined_storage_name
        self.file_attribute = file_attribute
        self.log_file = log_file
        self.model_name = model_name

    def _update_entry(self, key):
        if not self.reverse:
            self.database[key] = '1'
        else:
            try:
                del self.database[key]
            except KeyError:
                pass

    def _inclusion_condition(self, key):
        if self.reverse:
            return key in self.database
        else:
            return key not in self.database

    def execute(self, reverse=False):
        self.reverse = reverse
        model = apps.get_model(
            app_label=self.app_label, model_name=self.model_name
        )

        storage_instance = DefinedStorage.get(
            name=self.defined_storage_name
        ).get_storage_instance()

        if isinstance(storage_instance, PassthroughStorage):
            ContentType = apps.get_model(
                app_label='contenttypes', model_name='ContentType'
            )
            content_type = ContentType.objects.get_for_model(model=model)

            self.database = dbm.open(self.log_file, flag='c')

            for instance in model.objects.all():
                key = '{}.{}'.format(content_type.name, instance.pk)
                if self._inclusion_condition(key=key):
                    file_name = getattr(instance, self.file_attribute).name

                    content = storage_instance.open(
                        name=file_name, mode='rb',
                        _direct=not self.reverse
                    )
                    storage_instance.delete(name=file_name)
                    storage_instance.save(
                        name=file_name, content=content,
                        _direct=self.reverse
                    )
                    self._update_entry(key=key)

            self.database.close


def TemporaryFile(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.TemporaryFile(*args, **kwargs)


def fs_cleanup(filename, suppress_exceptions=True):
    """
    Tries to remove the given filename. Ignores non-existent files.
    """
    try:
        os.remove(filename)
    except OSError:
        try:
            shutil.rmtree(path=filename)
        except OSError:
            if suppress_exceptions:
                pass
            else:
                raise


def get_storage_subclass(dotted_path):
    """
    Import a storage class and return a subclass that will always return eq
    True to avoid creating a new migration when for runtime storage class
    changes. Used now only by historic migrations.
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
    """
    Creates a temporary directory in the most secure manner possible.
    There are no race conditions in the directory's creation.
    The directory is readable, writable, and searchable only by the creating
    user ID.
    """
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.mkdtemp(*args, **kwargs)


def mkstemp(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.mkstemp(*args, **kwargs)


def patch_files(path=None, replace_list=None):
    """
    Search and replace content from a list of file based on a pattern
    replace_list[
        {
            'filename_pattern': '*.css',
            'content_patterns': [
                {
                    'search': '',
                    'replace': '',
                }
            ]
        }
    ]
    """
    file_open_mode = 'r+'

    path_object = Path(path)
    for replace_entry in replace_list or []:
        for path_entry in path_object.glob('**/{}'.format(replace_entry['filename_pattern'])):
            if path_entry.is_file():
                for pattern in replace_entry['content_patterns']:
                    with path_entry.open(mode=file_open_mode) as source_file_object:
                        with tempfile.TemporaryFile(mode=file_open_mode) as temporary_file_object:
                            source_position = 0
                            destination_position = 0

                            while(True):
                                source_file_object.seek(source_position)
                                letter = source_file_object.read(1)

                                if len(letter) == 0:
                                    break
                                else:
                                    if letter == pattern['search'][0]:
                                        text = '{}{}'.format(letter, source_file_object.read(len(pattern['search']) - 1))

                                        temporary_file_object.seek(destination_position)
                                        if text == pattern['search']:
                                            text = pattern['replace']
                                            source_position = source_position + len(pattern['search'])
                                            destination_position = destination_position + len(pattern['replace'])
                                            temporary_file_object.write(text)

                                        else:
                                            source_position = source_position + 1
                                            destination_position = destination_position + 1
                                            temporary_file_object.write(letter)
                                    else:
                                        source_position = source_position + 1
                                        destination_position = destination_position + 1
                                        temporary_file_object.write(letter)

                            source_file_object.seek(0)
                            source_file_object.truncate()
                            temporary_file_object.seek(0)
                            shutil.copyfileobj(
                                fsrc=temporary_file_object,
                                fdst=source_file_object
                            )


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
