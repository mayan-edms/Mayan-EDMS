from __future__ import unicode_literals

import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        if hasattr(request, 'session'):
            tzname = request.session.get('django_timezone')
            if tzname:
                timezone.activate(pytz.timezone(tzname))
            else:
                timezone.deactivate()
        else:
            # TODO: Cookie, browser based timezone
            timezone.deactivate()
