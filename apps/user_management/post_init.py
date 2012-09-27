from __future__ import absolute_import

from south.signals import post_migrate

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, register_multi_item_links

from .links import (user_list, user_edit, user_add, user_delete,
    user_multiple_delete, user_set_password, user_multiple_set_password,
    group_list, group_edit, group_add, group_delete,
    group_multiple_delete, group_members)
from .models import AutoAdminSingleton
from .settings import (AUTO_CREATE_ADMIN, AUTO_ADMIN_USERNAME,
    AUTO_ADMIN_PASSWORD)


@receiver(post_migrate, dispatch_uid='create_superuser')
def create_superuser(sender, **kwargs):
    """
    From https://github.com/lambdalisue/django-qwert/blob/master/qwert/autoscript/__init__.py
    From http://stackoverflow.com/questions/1466827/ --

    Prevent interactive question about wanting a superuser created. (This code
    has to go in this otherwise empty "models" module so that it gets processed by
    the "syncdb" command during database creation.)

    Create our own admin super user automatically.
    """

    if AUTO_CREATE_ADMIN and kwargs['app'] == 'user_management':
        try:
            auth_models.User.objects.get(username=AUTO_ADMIN_USERNAME)
        except auth_models.User.DoesNotExist:
            print '*' * 80
            print 'Creating super admin user -- login: %s, password: %s' % (AUTO_ADMIN_USERNAME, AUTO_ADMIN_PASSWORD)
            print '*' * 80
            assert auth_models.User.objects.create_superuser(AUTO_ADMIN_USERNAME, 'autoadmin@autoadmin.com', AUTO_ADMIN_PASSWORD)
            admin = auth_models.User.objects.get(username=AUTO_ADMIN_USERNAME)
            # Store the auto admin password properties to display the first login message
            auto_admin_properties = AutoAdminSingleton.get()
            auto_admin_properties.account = admin
            auto_admin_properties.password = AUTO_ADMIN_PASSWORD
            auto_admin_properties.password_hash = admin.password
            auto_admin_properties.save()
        else:
            print 'Super admin user already exists. -- login: %s' % AUTO_ADMIN_USERNAME


@receiver(post_save, dispatch_uid='auto_admin_account_passwd_change', sender=User)
def auto_admin_account_passwd_change(sender, instance, **kwargs):
    auto_admin_properties = AutoAdminSingleton.get()
    if instance == auto_admin_properties.account and instance.password != auto_admin_properties.password_hash:
        # Only delete the auto admin properties when the password has been changed
        auto_admin_properties.delete(force=True)


bind_links([User], [user_edit, user_set_password, user_delete])
bind_links(['user_multiple_set_password', 'user_set_password', 'user_multiple_delete', 'user_delete', 'user_edit', 'user_list', 'user_add'], [user_list, user_add], menu_name=u'secondary_menu')
register_multi_item_links(['user_list'], [user_multiple_set_password, user_multiple_delete])

bind_links([Group], [group_edit, group_members, group_delete])
bind_links(['group_multiple_delete', 'group_delete', 'group_edit', 'group_list', 'group_add', 'group_members'], [group_list, group_add], menu_name=u'secondary_menu')
register_multi_item_links(['group_list'], [group_multiple_delete])
