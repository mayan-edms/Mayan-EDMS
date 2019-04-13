from __future__ import unicode_literals

import logging
import os
import shutil
import tempfile

from .settings import setting_temporary_directory

logger = logging.getLogger(__name__)


def TemporaryFile(*args, **kwargs):
    kwargs.update({'dir': setting_temporary_directory.value})
    return tempfile.TemporaryFile(*args, **kwargs)


# http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(source, destination, buffer_size=1024 * 1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    source_descriptor = get_descriptor(source)
    destination_descriptor = get_descriptor(destination, read=False)

    while True:
        copy_buffer = source_descriptor.read(buffer_size)
        if copy_buffer:
            destination_descriptor.write(copy_buffer)
        else:
            break

    source_descriptor.close()
    destination_descriptor.close()


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


def get_descriptor(file_input, read=True):
    try:
        # Is it a file like object?
        file_input.seek(0)
    except AttributeError:
        # If not, try open it.
        if read:
            return open(file_input, mode='rb')
        else:
            return open(file_input, mode='wb')
    else:
        return file_input


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
