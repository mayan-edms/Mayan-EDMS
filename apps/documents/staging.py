import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

from documents.conf.settings import STAGING_DIRECTORY    


def get_all_files():
    return sorted([os.path.normcase(f) for f in os.listdir(STAGING_DIRECTORY) if os.path.isfile(os.path.join(STAGING_DIRECTORY, f))])


class StagingFile(object):
    @classmethod
    def get_all(cls):
        staging_files = []
        for id, filename in enumerate(get_all_files()):
            staging_files.append(StagingFile(
                filepath=os.path.join(STAGING_DIRECTORY, filename),
                id=id))
        
        return staging_files

    @classmethod
    def get(cls, id):
        files = get_all_files()
        if id <= len(files):
            return StagingFile(
                filepath=os.path.join(STAGING_DIRECTORY, files[id]),
                id=id)
        raise ObjectDoesNotExist

    def __init__(self, filepath, id):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self._id = id
        
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
        return SimpleUploadedFile(name=self.filename, content=open(self.filepath).read())

        #return InMemoryUploadedFile(
        #    file=open(self.filepath, 'r'),
        #    field_name='',
        #    name=self.filename,
        #    content_type='unknown',
        #    size=os.path.getsize(self.filepath),
        #    charset=None,
        #)
