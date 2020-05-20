from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class ErrorLogEntryManager(models.Manager):
    def register(self, model):
        ErrorLogEntry = apps.get_model(
            app_label='common', model_name='ErrorLogEntry'
        )
        model.add_to_class(
            name='error_logs', value=GenericRelation(ErrorLogEntry)
        )


class UserLocaleProfileManager(models.Manager):
    def get_by_natural_key(self, user_natural_key):
        User = get_user_model()
        try:
            user = User.objects.get_by_natural_key(user_natural_key)
        except User.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(user__pk=user.pk)
