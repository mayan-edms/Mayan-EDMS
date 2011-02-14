from django.conf import settings

TEMPORARY_DIRECTORY = getattr(settings, 'COMMON_TEMPORARY_DIRECTORY', u'/tmp')
