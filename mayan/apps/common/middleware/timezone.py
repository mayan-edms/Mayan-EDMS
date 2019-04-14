from __future__ import unicode_literals

import pytz

from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'session'):
            tzname = request.session.get(settings.TIMEZONE_SESSION_KEY)
        else:
            tzname = request.COOKIES.get(settings.TIMEZONE_COOKIE_NAME)

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
