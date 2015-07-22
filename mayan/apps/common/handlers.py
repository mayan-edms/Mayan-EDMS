from __future__ import unicode_literals

from django.conf import settings
from django.utils import timezone, translation

from .models import UserLocaleProfile


def user_locale_profile_session_config(sender, request, user, **kwargs):
    user_locale_profile, created = UserLocaleProfile.objects.get_or_create(
        user=user
    )

    if not created and user_locale_profile.timezone and user_locale_profile.language:
        # Don't try to set locale preferences for new users or existing users
        # that have not set any preferences
        timezone.activate(user_locale_profile.timezone)
        translation.activate(user_locale_profile.language)

        if hasattr(request, 'session'):
            request.session[
                translation.LANGUAGE_SESSION_KEY
            ] = user_locale_profile.language
            request.session[
                settings.TIMEZONE_SESSION_KEY
            ] = user_locale_profile.timezone
        else:
            request.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, user_locale_profile.language
            )
            request.set_cookie(
                settings.TIMEZONE_COOKIE_NAME, user_locale_profile.timezone
            )


def user_locale_profile_create(sender, instance, created, **kwargs):
    if created:
        UserLocaleProfile.objects.create(user=instance)
