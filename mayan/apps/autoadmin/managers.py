from __future__ import unicode_literals

import logging

from django.contrib.auth import get_user_model
from django.core import management
from django.db import models

from .settings import setting_email, setting_password, setting_username

logger = logging.getLogger(name=__name__)


class AutoAdminSingletonManager(models.Manager):
    def create_autoadmin(self):
        UserModel = get_user_model()

        if setting_password.value is None:
            password = UserModel.objects.make_random_password()
        else:
            password = setting_password.value

        try:
            UserModel.objects.get(
                **{UserModel.USERNAME_FIELD: setting_username.value}
            )
        except UserModel.DoesNotExist:
            logger.info(
                'Creating superuser -- login: %s, email: %s, password: %s',
                setting_username.value, setting_email.value, password
            )
            management.call_command(
                'createsuperuser',
                **{
                    UserModel.USERNAME_FIELD: setting_username.value,
                    'email': setting_email.value,
                    'interactive': False
                }
            )

            account = UserModel.objects.get(
                **{UserModel.USERNAME_FIELD: setting_username.value}
            )
            account.set_password(raw_password=password)
            account.save()
            # Store the auto admin password properties to display the
            # first login message
            auto_admin_properties, created = self.get_or_create()  # NOQA
            auto_admin_properties.account = account
            auto_admin_properties.password = password
            auto_admin_properties.password_hash = account.password
            auto_admin_properties.save()
        else:
            logger.error(
                'Super admin user already exists. -- login: %s',
                setting_username.value
            )
