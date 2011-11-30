import errno
import os

from django.utils.translation import ugettext_lazy as _

from document_indexing.os_agnostic import assemble_document_filename
from document_indexing.conf.settings import FILESERVING_ENABLE
from document_indexing.conf.settings import FILESERVING_PATH


def get_instance_path(index_instance):
    """
    Return a platform formated filesytem path corresponding to an
    index instance
    """
    names = []
    for ancestor in index_instance.get_ancestors():
        names.append(ancestor.value)

    names.append(index_instance.value)

    return os.sep.join(names)


def fs_create_index_directory(index_instance):
    if FILESERVING_ENABLE:
        target_directory = os.path.join(FILESERVING_PATH, get_instance_path(index_instance))
        try:
            os.mkdir(target_directory)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise Exception(_(u'Unable to create indexing directory; %s') % exc)


def fs_create_document_link(index_instance, document, suffix=0):
    if FILESERVING_ENABLE:
        filename = assemble_document_filename(document.file_filename, suffix)
        filepath = os.path.join(FILESERVING_PATH, get_instance_path(index_instance), filename)
        try:
            os.symlink(document.file.path, filepath)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                # This link should not exist, try to delete it
                try:
                    os.unlink(filepath)
                    # Try again
                    os.symlink(document.file.path, filepath)
                except Exception, exc:
                    raise Exception(_(u'Unable to create symbolic link, file exists and could not be deleted: %(filepath)s; %(exc)s') % {'filepath': filepath, 'exc': exc})
            else:
                raise Exception(_(u'Unable to create symbolic link: %(filepath)s; %(exc)s') % {'filepath': filepath, 'exc': exc})


def fs_delete_document_link(index_instance, document, suffix=0):
    if FILESERVING_ENABLE:
        filename = assemble_document_filename(document.file_filename, suffix)
        filepath = os.path.join(FILESERVING_PATH, get_instance_path(index_instance), filename)

        try:
            os.unlink(filepath)
        except OSError, exc:
            if exc.errno != errno.ENOENT:
                # Raise when any error other than doesn't exits
                raise Exception(_(u'Unable to delete document symbolic link; %s') % exc)


def fs_delete_index_directory(index_instance):
    if FILESERVING_ENABLE:
        target_directory = os.path.join(FILESERVING_PATH, get_instance_path(index_instance))
        try:
            os.removedirs(target_directory)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise Exception(_(u'Unable to delete indexing directory; %s') % exc)


def fs_delete_directory_recusive(path=FILESERVING_PATH):
    if FILESERVING_ENABLE:
        for dirpath, dirnames, filenames in os.walk(path, topdown=False):
            for filename in filenames:
                os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                os.rmdir(os.path.join(dirpath, dirname))
