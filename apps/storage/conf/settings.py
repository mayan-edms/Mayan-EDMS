from django.conf import settings


GRIDFS_HOST = getattr(settings, 'STORAGE_GRIDFS_HOST', 'localhost')
GRIDFS_PORT = getattr(settings, 'STORAGE_GRIDFS_PORT', 27017)
DATABASE_NAME = getattr(settings, 'STORAGE_GRIDFS_DATABASE_NAME', u'document_storage')
