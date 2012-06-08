from __future__ import absolute_import

import tempfile

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.dispatch import receiver
from django.db.models.signals import post_syncdb

from navigation.api import bind_links, register_top_menu, Link

from .conf.settings import (AUTO_CREATE_ADMIN, AUTO_ADMIN_USERNAME,
    AUTO_ADMIN_PASSWORD, TEMPORARY_DIRECTORY)
from .conf import settings as common_settings
from .utils import validate_path


def has_usable_password(context):
    return context['request'].user.has_usable_password

password_change_view = Link(text=_(u'change password'), view='password_change_view', sprite='computer_key', condition=has_usable_password)
current_user_details = Link(text=_(u'user details'), view='current_user_details', sprite='vcard')
current_user_edit = Link(text=_(u'edit details'), view='current_user_edit', sprite='vcard_edit')
about_view = Link(text=_('about'), view='about_view', sprite='information')
license_view = Link(text=_('license'), view='license_view', sprite='script')

bind_links(['about_view', 'license_view'], [about_view, license_view], menu_name='secondary_menu')
bind_links(['current_user_details', 'current_user_edit', 'password_change_view'], [current_user_details, current_user_edit, password_change_view], menu_name='secondary_menu')

register_top_menu('about', link=Link(text=_(u'about'), view='about_view', sprite='information'), position=-1)


@receiver(post_syncdb, dispatch_uid='create_superuser_processor', sender=auth_models)
def create_superuser_processor(sender, **kwargs):
    """
    From https://github.com/lambdalisue/django-qwert/blob/master/qwert/autoscript/__init__.py
    From http://stackoverflow.com/questions/1466827/ --

    Prevent interactive question about wanting a superuser created. (This code
    has to go in this otherwise empty "models" module so that it gets processed by
    the "syncdb" command during database creation.)

    Create our own admin super user automatically.
    """

    if AUTO_CREATE_ADMIN:
        try:
            auth_models.User.objects.get(username=AUTO_ADMIN_USERNAME)
        except auth_models.User.DoesNotExist:
            print '*' * 80
            print 'Creating super admin user -- login: %s, password: %s' % (AUTO_ADMIN_USERNAME, AUTO_ADMIN_PASSWORD)
            print '*' * 80
            assert auth_models.User.objects.create_superuser(AUTO_ADMIN_USERNAME, 'x@x.com', AUTO_ADMIN_PASSWORD)
        else:
            print 'Super admin user already exists. -- login: %s' % AUTO_ADMIN_USERNAME

if (validate_path(TEMPORARY_DIRECTORY) == False) or (not TEMPORARY_DIRECTORY):
    setattr(common_settings, 'TEMPORARY_DIRECTORY', tempfile.mkdtemp())
