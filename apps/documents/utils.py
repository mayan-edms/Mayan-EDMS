import os

from common.conf.settings import TEMPORARY_DIRECTORY

def document_save_to_temp_dir(document, filename, buffer_size=1024 * 1024):
    temporary_path = os.path.join(TEMPORARY_DIRECTORY, filename)
    return document.save_to_file(temporary_path, buffer_size)
