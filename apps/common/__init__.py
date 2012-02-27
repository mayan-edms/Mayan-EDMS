from __future__ import absolute_import

import tempfile

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.dispatch import receiver
from django.db.models.signals import post_syncdb

from navigation.api import register_links, register_top_menu

from .conf import settings as common_settings
from .utils import validate_path


def has_usable_password(context):
    return context['request'].user.has_usable_password

password_change_view = {'text': _(u'change password'), 'view': 'password_change_view', 'famfam': 'computer_key', 'condition': has_usable_password}
current_user_details = {'text': _(u'user details'), 'view': 'current_user_details', 'famfam': 'vcard'}
current_user_edit = {'text': _(u'edit details'), 'view': 'current_user_edit', 'famfam': 'vcard_edit'}

register_links(['current_user_details', 'current_user_edit', 'password_change_view'], [current_user_details, current_user_edit, password_change_view], menu_name='secondary_menu')

about_view = {'text': _('about'), 'view': 'about_view', 'famfam': 'information'}
license_view = {'text': _('license'), 'view': 'license_view', 'famfam': 'script'}

register_links(['about_view', 'license_view'], [about_view, license_view], menu_name='secondary_menu')

register_top_menu('about', link={'text': _(u'about'), 'view': 'about_view', 'famfam': 'information'}, position=-1)


@receiver(post_syncdb, dispatch_uid='create_superuser', sender=auth_models)
def create_superuser(sender, **kwargs):
    """
    From https://github.com/lambdalisue/django-qwert/blob/master/qwert/autoscript/__init__.py
    From http://stackoverflow.com/questions/1466827/ --

    Prevent interactive question about wanting a superuser created. (This code
    has to go in this otherwise empty "models" module so that it gets processed by
    the "syncdb" command during database creation.)

    Create our own admin super user automatically.
    """

    if common_settings.AUTO_CREATE_ADMIN:
        USERNAME = common_settings.AUTO_ADMIN_USERNAME
        PASSWORD = common_settings.AUTO_ADMIN_PASSWORD
        try:
            auth_models.User.objects.get(username=USERNAME)
        except auth_models.User.DoesNotExist:
            print '*' * 80
            print 'Creating super admin user -- login: %s, password: %s' % (USERNAME, PASSWORD)
            print '*' * 80
            assert auth_models.User.objects.create_superuser(USERNAME, 'x@x.com', PASSWORD)
        else:
            print 'Super admin user already exists. -- login: %s, password: %s' % (USERNAME, PASSWORD)

if (validate_path(common_settings.TEMPORARY_DIRECTORY) == False) or (not common_settings.TEMPORARY_DIRECTORY):
    setattr(common_settings, 'TEMPORARY_DIRECTORY', tempfile.mkdtemp())
