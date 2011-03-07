import os
import tempfile


from common import TEMPORARY_DIRECTORY


#http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(source, dest, buffer_size=1024*1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    if not hasattr(source, 'read'):
        source = open(source, 'rb')
    if not hasattr(dest, 'write'):
        dest = open(dest, 'wb')

    while True:
        copy_buffer = source.read(buffer_size)
        if copy_buffer:
            dest.write(copy_buffer)
        else:
            break

    source.close()
    dest.close()


def document_save_to_temp_dir(document, filename, buffer_size=1024*1024):
    temporary_path = os.path.join(TEMPORARY_DIRECTORY, filename)
    return document.save_to_file(temporary_path, buffer_size)


