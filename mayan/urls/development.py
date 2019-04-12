from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url

from .base import *  # NOQA

if 'rosetta' in settings.INSTALLED_APPS:
    try:
        import rosetta  # NOQA
    except ImportError:
        pass
    else:
        urlpatterns += [  # NOQA
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta')
        ]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns += [  # NOQA
            url(r'^__debug__/', include(debug_toolbar.urls))
        ]
