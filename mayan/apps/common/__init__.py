from __future__ import absolute_import, unicode_literals

import logging
import tempfile

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from south.signals import post_migrate

from common import settings as common_settings
from navigation.api import register_links, register_top_menu

from .links import (
    link_about, link_current_user_details, link_current_user_edit,
    link_current_user_locale_profile_details,
    link_current_user_locale_profile_edit, link_license, link_logout,
    link_password_change
)
from .models import (
    AnonymousUserSingleton, AutoAdminSingleton, UserLocaleProfile
)
from .settings import (
    AUTO_ADMIN_USERNAME, AUTO_ADMIN_PASSWORD, AUTO_CREATE_ADMIN,
    TEMPORARY_DIRECTORY
)
from .utils import validate_path

logger = logging.getLogger(__name__)

register_links(['common:current_user_details', 'common:current_user_edit', 'common:current_user_locale_profile_details', 'common:current_user_locale_profile_edit', 'common:password_change_view'], [link_current_user_details, link_current_user_edit, link_current_user_locale_profile_details, link_current_user_locale_profile_edit, link_password_change, link_logout], menu_name='secondary_menu')
register_links(['common:about_view', 'common:license_view', 'registration:form_view'], [link_about, link_license], menu_name='secondary_menu')

register_top_menu('about', link_about, position=-1)


@receiver(post_migrate, dispatch_uid='create_superuser_and_anonymous_user')
def create_superuser_and_anonymous_user(sender, **kwargs):
    """
    From https://github.com/lambdalisue/django-qwert/blob/master/qwert/autoscript/__init__.py
    From http://stackoverflow.com/questions/1466827/ --

    Prevent interactive question about wanting a superuser created. (This code
    has to go in this otherwise empty "models" module so that it gets processed by
    the "syncdb" command during database creation.)

    Create our own admin super user automatically.
    """
    if kwargs['app'] == 'common':
        AutoAdminSingleton.objects.get_or_create()
        AnonymousUserSingleton.objects.get_or_create()

        if AUTO_CREATE_ADMIN:
            try:
                auth_models.User.objects.get(username=AUTO_ADMIN_USERNAME)
            except auth_models.User.DoesNotExist:
                logger.info('Creating super admin user -- login: %s, password: %s', AUTO_ADMIN_USERNAME, AUTO_ADMIN_PASSWORD)
                assert auth_models.User.objects.create_superuser(AUTO_ADMIN_USERNAME, 'autoadmin@autoadmin.com', AUTO_ADMIN_PASSWORD)
                admin = auth_models.User.objects.get(username=AUTO_ADMIN_USERNAME)
                # Store the auto admin password properties to display the first login message
                auto_admin_properties, created = AutoAdminSingleton.objects.get_or_create()
                auto_admin_properties.account = admin
                auto_admin_properties.password = AUTO_ADMIN_PASSWORD
                auto_admin_properties.password_hash = admin.password
                auto_admin_properties.save()
            else:
                logger.info('Super admin user already exists. -- login: %s', AUTO_ADMIN_USERNAME)


@receiver(post_save, dispatch_uid='auto_admin_account_passwd_change', sender=User)
def auto_admin_account_passwd_change(sender, instance, **kwargs):
    auto_admin_properties = AutoAdminSingleton.objects.get()
    if instance == auto_admin_properties.account and instance.password != auto_admin_properties.password_hash:
        # Only delete the auto admin properties when the password has been changed
        auto_admin_properties.account = None
        auto_admin_properties.password = None
        auto_admin_properties.password_hash = None
        auto_admin_properties.save()


@receiver(user_logged_in, dispatch_uid='user_locale_profile_session_config', sender=User)
def user_locale_profile_session_config(sender, request, user, **kwargs):
    if hasattr(request, 'session'):
        user_locale_profile, created = UserLocaleProfile.objects.get_or_create(user=user)
        request.session['django_language'] = user_locale_profile.language
        request.session['django_timezone'] = user_locale_profile.timezone
    else:
        request.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_locale_profile.language)


@receiver(post_save, dispatch_uid='user_locale_profile_create', sender=User)
def user_locale_profile_create(sender, instance, created, **kwargs):
    if created:
        UserLocaleProfile.objects.create(user=instance)


if (not validate_path(TEMPORARY_DIRECTORY)) or (not TEMPORARY_DIRECTORY):
    setattr(common_settings, 'TEMPORARY_DIRECTORY', tempfile.mkdtemp())
