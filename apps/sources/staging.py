import errno
import os
import hashlib

from django.core.files.base import File
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from converter import TRANFORMATION_CHOICES
from converter.api import convert, cache_cleanup

DEFAULT_STAGING_DIRECTORY = u'/tmp'
#from documents.conf.settings import DEFAULT_TRANSFORMATIONS

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
        raise OSError(ugettext(u'Unable get list of staging files: %s') % exc)


def _return_new_class():
    return type('StagingFile', (StagingFile,), dict(StagingFile.__dict__))


def create_staging_file_class(request, source):
    cls = _return_new_class()
    #cls.set_path(evaluate_user_staging_path(request, source))
    cls.set_path(source)
    return cls


class StagingFile(object):
    """
    Simple class to encapsulate the files in a directory and hide the
    specifics to the view
    """
    path = DEFAULT_STAGING_DIRECTORY

    @classmethod
    def set_path(cls, path):
        cls.path = path

    @classmethod
    def get_all(cls):
        """
        Return a list of StagingFile instances corresponding to the
        current path
        """
        staging_files = []
        for filename in get_all_files(cls.path):
            staging_files.append(StagingFile(
                filepath=os.path.join(cls.path, filename)))

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

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self._id = HASH_FUNCTION(open(filepath).read())

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
        allow for easier upload a staging files
        """
        try:
            return File(file(self.filepath, 'rb'), name=self.filename)
        except Exception, exc:
            raise Exception(ugettext(u'Unable to upload staging file: %s') % exc)

    def delete(self, preview_size):
        # tranformation_string, errors = get_transformation_string(DEFAULT_TRANSFORMATIONS)
        cache_cleanup(self.filepath, size=preview_size)# , extra_options=tranformation_string)
        try:
            os.unlink(self.filepath)
        except OSError, exc:
            if exc.errno == errno.ENOENT:
                pass
            else:
                raise OSError(ugettext(u'Unable to delete staging file: %s') % exc)

    def preview(self, preview_size):
        errors = []
        # tranformation_string, errors = get_transformation_string(DEFAULT_TRANSFORMATIONS)
        # output_file = convert(self.filepath, size=STAGING_FILES_PREVIEW_SIZE, extra_options=tranformation_string, cleanup_files=False)
        output_file = convert(self.filepath, size=preview_size, cleanup_files=False)
        return output_file, errors


def get_transformation_string(transformations):
    transformation_list = []
    errors = []
    for transformation in transformations:
        try:
            if transformation['name'] in TRANFORMATION_CHOICES:
                output = TRANFORMATION_CHOICES[transformation['name']] % eval(transformation['arguments'])
                transformation_list.append(output)
        except Exception, e:
            errors.append(e)

    tranformation_string = ' '.join(transformation_list)
    return tranformation_string, errors
