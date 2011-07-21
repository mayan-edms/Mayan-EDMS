import os

from common.conf.settings import TEMPORARY_DIRECTORY

try:
    from python_magic import magic
    USE_PYTHON_MAGIC = True
except:
    import mimetypes
    mimetypes.init()
    USE_PYTHON_MAGIC = False


#http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(source, dest, buffer_size=1024 * 1024):
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


def document_save_to_temp_dir(document, filename, buffer_size=1024 * 1024):
    temporary_path = os.path.join(TEMPORARY_DIRECTORY, filename)
    return document.save_to_file(temporary_path, buffer_size)


def get_document_mimetype(document):
    """
    Determine a documents mimetype by calling the system's libmagic
    library via python-magic or fallback to use python's mimetypes
    library
    """
    file_mimetype = u''
    file_mime_encoding = u''

    if USE_PYTHON_MAGIC:
        if document.exists():
            try:
                source = document.open()
                mime = magic.Magic(mime=True)
                file_mimetype = mime.from_buffer(source.read())
                source.seek(0)
                mime_encoding = magic.Magic(mime_encoding=True)
                file_mime_encoding = mime_encoding.from_buffer(source.read())
            finally:
                if source:
                    source.close()
    else:
        file_mimetype, file_mime_encoding = mimetypes.guess_type(document.get_fullname())

    return file_mimetype, file_mime_encoding
