from django.utils.translation import ugettext_lazy as _

from drf_yasg import openapi

import mayan
from mayan.apps.common.settings import setting_project_title

from .literals import API_VERSION

openapi_info = openapi.Info(
    title=_('%s API') % setting_project_title.value,
    default_version='v{}'.format(API_VERSION),
    description=mayan.__description__,
    license=openapi.License(name=mayan.__license__)
)
