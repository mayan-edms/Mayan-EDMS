from __future__ import absolute_import

import errno
import os
import hashlib

from django.core.files.base import File
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext
from django.utils.encoding import smart_str

from documents.settings import THUMBNAIL_SIZE

#from mimetype.api import (get_icon_file_path, get_error_icon_file_path,
from mimetype.api import get_mimetype
from converter.api import convert, cache_cleanup
from converter.exceptions import UnknownFileFormat, UnkownConvertError


DEFAULT_STAGING_DIRECTORY = u'/tmp'

HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()
#TODO: Do benchmarks
#func = lambda:[StagingFile.get_all() is None for i in range(100)]
#t1=time.time();func();t2=time.time();print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)

#STAGING_FILE_FUNCTIONS = {
#    UPLOAD_SOURCE_STAGING: lambda x: STAGING_DIRECTORY,
#    UPLOAD_SOURCE_USER_STAGING: lambda x: os.path.join(USER_STAGING_DIRECTORY_ROOT, eval(USER_STAGING_DIRECTORY_EXPRESSION, {'user': x.user}))
#}


#def evaluate_user_staging_path(request, source):
#    try:
#        return STAGING_FILE_FUNCTIONS[source](request)
#    except Exception, exc:
#        messages.error(request, _(u'Error evaluating user staging directory expression; %s') % exc)
#        return u''


def get_all_files(path):
    try:
        return sorted([os.path.normcase(f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    except OSError, exc:
        raise Exception(ugettext(u'Unable get list of staging files: %s') % exc)


def _return_new_class():
    return type('StagingFile', (StagingFile,), dict(StagingFile.__dict__))


def create_staging_file_class(request, directory_path, source=None):
    cls = _return_new_class()
    #cls.set_path(evaluate_user_staging_path(request, source))
    cls.set_path(directory_path)
    if source is not None:
        cls.set_source(source)
    return cls


class StagingFile(object):
    """
    Simple class to encapsulate the files in a directory and hide the
    specifics to the view
    """
    path = DEFAULT_STAGING_DIRECTORY
    source = None

    @classmethod
    def set_path(cls, path):
        cls.path = path

    @classmethod
    def set_source(cls, source):
        cls.source = source

    @classmethod
    def get_all(cls):
        """
        Return a list of StagingFile instances corresponding to the
        current path
        """
        staging_files = []
        for filename in get_all_files(cls.path):
            staging_files.append(StagingFile(
                filepath=os.path.join(cls.path, filename), source=cls.source))

        return staging_files

    @classmethod
    def get(cls, id):
        """
        Return a single StagingFile instance corresponding to the id
        given as argument
        """
        files_dict = dict([(file.id, file) for file in cls.get_all()])
        if id in files_dict:
            return files_dict[id]
        else:
            raise ObjectDoesNotExist

    def __init__(self, filepath, source=None):
        self.source = source
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self._id = HASH_FUNCTION(smart_str(filepath))

    def __unicode__(self):
        return self.filename

    def __repr__(self):
        return self.__unicode__()

    def __getattr__(self, name):
        if name == 'id':
            return self._id
        else:
            raise AttributeError

    def upload(self):
        """
        Return a StagingFile encapsulated in a File class instance to
        allow for easier upload of staging files
        """
        try:
            return File(file(self.filepath, 'rb'), name=self.filename)
        except Exception, exc:
            raise Exception(ugettext(u'Unable to upload staging file: %s') % exc)

    def delete(self, preview_size, transformations):
        cache_cleanup(self.filepath, size=preview_size, transformations=transformations)
        try:
            os.unlink(self.filepath)
        except OSError, exc:
            if exc.errno == errno.ENOENT:
                pass
            else:
                raise Exception(ugettext(u'Unable to delete staging file: %s') % exc)

    def get_valid_image(self, size=THUMBNAIL_SIZE, transformations=None):
        return convert(self.filepath, size=size, cleanup_files=False, transformations=transformations)

    def get_image(self, size, transformations):
        try:
            return self.get_valid_image(size=size, transformations=transformations)
            #return convert(self.filepath, size=size, cleanup_files=False, transformations=transformations)
        except UnknownFileFormat:
            mimetype, encoding = get_mimetype(open(self.filepath, 'rb'), self.filepath)
            # TODO: Fix
            return ''#get_icon_file_path(mimetype)
        except UnkownConvertError:
            return get_error_icon_file_path()
