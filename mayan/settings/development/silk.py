from .base import *  # NOQA

if 'silk' not in INSTALLED_APPS:  # NOQA: F405
    INSTALLED_APPS += (  # NOQA: F405
        'silk',
    )

MIDDLEWARE = (
    'silk.middleware.SilkyMiddleware',
) + MIDDLEWARE  # NOQA: F405
