import errno
import os
import hashlib

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.utils.translation import ugettext


from documents.conf.settings import STAGING_DIRECTORY    

HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()

#func = lambda:[StagingFile.get_all() is None for i in range(100)]
#t1=time.time();func();t2=time.time();print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)


def get_all_files():
    try:
        return sorted([os.path.normcase(f) for f in os.listdir(STAGING_DIRECTORY) if os.path.isfile(os.path.join(STAGING_DIRECTORY, f))])
    except OSError, exc:
        raise OSError(ugettext(u'Unable get list of staging files: %s') % exc)


class StagingFile(object):
    """
    Simple class to encapsulate the files in a directory and hide the 
    specifics to the view
    """
    @classmethod
    def get_all(cls):
        staging_files = []
        for filename in get_all_files():
            staging_files.append(StagingFile(
                filepath=os.path.join(STAGING_DIRECTORY, filename)))
                
        return staging_files

    @classmethod
    def get(cls, id):
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
            raise AttributeError, name
    
    def upload(self):
        try:
            return SimpleUploadedFile(name=self.filename, content=open(self.filepath).read())
        except Exception, exc:
            raise Exception(ugettext(u'Unable to upload staging file: %s') % exc)
    
    
        #return InMemoryUploadedFile(
        #    file=open(self.filepath, 'r'),
        #    field_name='',
        #    name=self.filename,
        #    content_type='unknown',
        #    size=os.path.getsize(self.filepath),
        #    charset=None,
        #)

    def delete(self):
        try:
            os.unlink(self.filepath)
        except OSError, exc:
            if exc.errno == errno.ENOENT:
                pass
            else: 
                raise OSError(ugettext(u'Unable to delete staging file: %s') % exc)
