from __future__ import unicode_literals

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import reverse

from .events import (
    event_group_created, event_group_edited, event_user_created,
    event_user_edited
)


def get_method_group_save():
    Group = apps.get_model(app_label='auth', model_name='Group')
    group_save_original = Group.save

    def method_group_save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            is_new = not self.pk
            group_save_original(self, *args, **kwargs)
            if is_new:
                event_group_created.commit(
                    actor=_user, target=self
                )
            else:
                event_group_edited.commit(
                    actor=_user, target=self
                )

    return method_group_save


def method_user_get_absolute_url(self):
    return reverse(
        viewname='user_management:user_details', kwargs={'pk': self.pk}
    )


def get_method_user_save():
    user_save_original = get_user_model().save

    def method_user_save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            is_new = not self.pk
            user_save_original(self, *args, **kwargs)
            if is_new:
                event_user_created.commit(
                    actor=_user, target=self
                )
            else:
                event_user_edited.commit(
                    actor=_user, target=self
                )

    return method_user_save
