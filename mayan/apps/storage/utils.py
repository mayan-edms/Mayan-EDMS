from __future__ import unicode_literals

import fileinput
import logging
import os
import shutil
import tempfile

from pathlib2 import Path

from django.utils.encoding import force_text
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
    path_object = Path(path)
    for replace_entry in replace_list or []:
        for path_entry in path_object.glob('**/{}'.format(replace_entry['filename_pattern'])):
            if path_entry.is_file():
                # PY3
                # Don't use context processor to allow working on Python 2.7
                # Update on Mayan EDMS version >= 4.0
                file_object = fileinput.FileInput(force_text(path_entry), inplace=True)
                for line in file_object:
                    for pattern in replace_entry['content_patterns']:
                        line = line.replace(pattern['search'], pattern['replace'])
                    print(line, end='')
                file_object.close()


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
