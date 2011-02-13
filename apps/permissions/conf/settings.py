from django.conf import settings

DEFAULT_ROLES = getattr(settings, 'ROLES_DEFAULT_ROLES', [])
