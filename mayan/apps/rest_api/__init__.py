from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .classes import APIEndPoint
from .urls import api_urls

endpoint = APIEndPoint('rest_api')
endpoint.register_urls(api_urls)
endpoint.add_endpoint('auth_token_obtain', _(u'Obtain an API authentication token.'))
