import tempfile

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

from navigation.api import register_links

from common.conf import settings as common_settings

TEMPORARY_DIRECTORY = common_settings.TEMPORARY_DIRECTORY \
    if common_settings.TEMPORARY_DIRECTORY else tempfile.mkdtemp()


def has_usable_password(context):
    return context['request'].user.has_usable_password

password_change_view = {'text': _(u'change password'), 'view': 'password_change_view', 'famfam': 'computer_key', 'condition': has_usable_password}
current_user_details = {'text': _(u'user details'), 'view': 'current_user_details', 'famfam': 'vcard'}
current_user_edit = {'text': _(u'edit details'), 'view': 'current_user_edit', 'famfam': 'vcard_edit'}

register_links(['current_user_details', 'current_user_edit', 'password_change_view'], [current_user_details, current_user_edit, password_change_view], menu_name='secondary_menu')


if common_settings.AUTO_CREATE_ADMIN:
    # From https://github.com/lambdalisue/django-qwert/blob/master/qwert/autoscript/__init__.py
    # From http://stackoverflow.com/questions/1466827/ --
    #
    # Prevent interactive question about wanting a superuser created. (This code
    # has to go in this otherwise empty "models" module so that it gets processed by
    # the "syncdb" command during database creation.)
    #
    # Create our own test user automatically.
    def create_testuser(app, created_models, verbosity, **kwargs):
        USERNAME = common_settings.AUTO_ADMIN_USERNAME
        PASSWORD = common_settings.AUTO_ADMIN_PASSWORD
        try:
            auth_models.User.objects.get(username=USERNAME)
        except auth_models.User.DoesNotExist:
            print '*' * 80
            print 'Creating test user -- login: %s, password: %s' % (USERNAME, PASSWORD)
            print '*' * 80
            assert auth_models.User.objects.create_superuser(USERNAME, 'x@x.com', PASSWORD)
        else:
            print 'Test user already exists. -- login: %s, password: %s' % (USERNAME, PASSWORD)
    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_models,
        dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(create_testuser,
        sender=auth_models, dispatch_uid='common.models.create_testuser')
