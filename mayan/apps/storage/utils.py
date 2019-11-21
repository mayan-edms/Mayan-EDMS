from __future__ import unicode_literals

import logging
import os
import shutil
import tempfile

from pathlib2 import Path

try:
    from django.utils.six import PY3
except ImportError:
    # This is being imported outside of Django
    import sys
    PY3 = sys.version_info[0] == 3
else:
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


def mkdtemp(*args, **kwargs):
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
    if PY3:
        file_open_mode = 'r+'
    else:
        file_open_mode = 'rb+'

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
                            shutil.copyfileobj(fsrc=temporary_file_object, fdst=source_file_object)


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
