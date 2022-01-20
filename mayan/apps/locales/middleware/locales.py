import pytz

from django.utils import timezone, translation
from django.utils.deprecation import MiddlewareMixin


class UserLocaleProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user:
            locale_profile = getattr(user, 'locale_profile', None)
            if locale_profile:
                if locale_profile.language:
                    translation.activate(language=locale_profile.language)

                if locale_profile.timezone:
                    timezone.activate(
                        timezone=pytz.timezone(zone=locale_profile.timezone)
                    )
                else:
                    timezone.deactivate()
