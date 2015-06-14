from __future__ import unicode_literals

from django.conf import settings

from .models import UserLocaleProfile


def user_locale_profile_session_config(sender, request, user, **kwargs):
    if hasattr(request, 'session'):
        user_locale_profile, created = UserLocaleProfile.objects.get_or_create(user=user)
        request.session['django_language'] = user_locale_profile.language
        request.session['django_timezone'] = user_locale_profile.timezone
    else:
        request.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_locale_profile.language)


def user_locale_profile_create(sender, instance, created, **kwargs):
    if created:
        UserLocaleProfile.objects.create(user=instance)
