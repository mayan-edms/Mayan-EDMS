from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from drf_yasg import openapi

import mayan

openapi_info = openapi.Info(
    title=_('%s API') % mayan.__title__,
    default_version='v2',
    description=mayan.__description__,
    license=openapi.License(name=mayan.__license__),
)
