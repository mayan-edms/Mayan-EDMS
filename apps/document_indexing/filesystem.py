from __future__ import absolute_import

import errno
import os

from django.utils.translation import ugettext_lazy as _


def assemble_suffixed_filename(filename, suffix=0):
    """
    Split document filename, to attach suffix to the name part then
    re attacht the extension
    """
    from .settings import SUFFIX_SEPARATOR

    if suffix:
        name, extension = os.path.splitext(filename)
        return SUFFIX_SEPARATOR.join([name, unicode(suffix), os.extsep, extension])
    else:
        return filename


def assemble_path_from_list(directory_list):
    return os.path.normpath(os.sep.join(directory_list))


def get_instance_path(index_instance):
    """
    Return a platform formated filesytem path corresponding to an
    index instance
    """
    names = []
    for ancestor in index_instance.get_ancestors():
        names.append(ancestor.value)

    names.append(index_instance.value)

    return assemble_path_from_list(names)


def fs_create_index_directory(index_instance):
    from .settings import FILESYSTEM_SERVING

    if index_instance.index_template_node.index.name in FILESYSTEM_SERVING:
        target_directory = assemble_path_from_list([FILESYSTEM_SERVING[index_instance.index_template_node.index.name], get_instance_path(index_instance)])
        try:
            os.mkdir(target_directory)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise Exception(_(u'Unable to create indexing directory; %s') % exc)


def fs_create_document_link(index_instance, document, suffix=0):
    from .settings import FILESYSTEM_SERVING

    if index_instance.index_template_node.index.name in FILESYSTEM_SERVING:
        filename = assemble_suffixed_filename(document.file_filename, suffix)
        filepath = assemble_path_from_list([FILESYSTEM_SERVING[index_instance.index_template_node.index.name], get_instance_path(index_instance), filename])

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
    from .settings import FILESYSTEM_SERVING

    if index_instance.index_template_node.index.name in FILESYSTEM_SERVING:
        filename = assemble_suffixed_filename(document.file_filename, suffix)
        filepath = assemble_path_from_list([FILESYSTEM_SERVING[index_instance.index_template_node.index.name], get_instance_path(index_instance), filename])

        try:
            os.unlink(filepath)
        except OSError, exc:
            if exc.errno != errno.ENOENT:
                # Raise when any error other than doesn't exits
                raise Exception(_(u'Unable to delete document symbolic link; %s') % exc)


def fs_delete_index_directory(index_instance):
    from .settings import FILESYSTEM_SERVING

    if index_instance.index_template_node.index.name in FILESYSTEM_SERVING:
        target_directory = assemble_path_from_list([FILESYSTEM_SERVING[index_instance.index_template_node.index.name], get_instance_path(index_instance)])
        try:
            os.removedirs(target_directory)
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise Exception(_(u'Unable to delete indexing directory; %s') % exc)


def fs_delete_directory_recusive(index):
    from .settings import FILESYSTEM_SERVING

    if index.name in FILESYSTEM_SERVING:
        path = FILESYSTEM_SERVING[index.name]
        for dirpath, dirnames, filenames in os.walk(path, topdown=False):
            for filename in filenames:
                os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                os.rmdir(os.path.join(dirpath, dirname))
