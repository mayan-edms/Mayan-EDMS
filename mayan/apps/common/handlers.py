from __future__ import unicode_literals

from django.conf import settings

from .models import (
    AnonymousUserSingleton, AutoAdminSingleton, UserLocaleProfile
)


def auto_admin_account_passwd_change(sender, instance, **kwargs):
    auto_admin_properties = AutoAdminSingleton.objects.get()
    if instance == auto_admin_properties.account and instance.password != auto_admin_properties.password_hash:
        # Only delete the auto admin properties when the password has been changed
        auto_admin_properties.account = None
        auto_admin_properties.password = None
        auto_admin_properties.password_hash = None
        auto_admin_properties.save()


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
