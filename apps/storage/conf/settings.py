from django.conf import settings


GRIDFS_HOST = getattr(settings, 'STORAGE_GRIDFS_HOST', u'localhost')
GRIDFS_PORT = getattr(settings, 'STORAGE_GRIDFS_PORT', 27017)
GRIDFS_DATABASE_NAME = getattr(settings, 'STORAGE_GRIDFS_DATABASE_NAME', u'document_storage')

FILESTORAGE_LOCATION = getattr(settings, 'STORAGE_FILESTORAGE_LOCATION', u'document_storage')
