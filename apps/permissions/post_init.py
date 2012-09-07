from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist


def user_post_save(sender, instance, **kwargs):
    from .settings import DEFAULT_ROLES

    if kwargs.get('created', False):
        for default_role in SETTING_DEFAULT_ROLES:
            if isinstance(default_role, Role):
                #If a model is passed, execute method
                default_role.add_member(instance)
            else:
                #If a role name is passed, lookup the corresponding model
                try:
                    role = Role.objects.get(name=default_role)
                    role.add_member(instance)
                except ObjectDoesNotExist:
                    pass


def init_signal_handler():
    post_save.connect(user_post_save, sender=User)
