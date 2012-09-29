from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from .settings import DEFAULT_ROLES
from .models import Role


@receiver(post_save, dispatch_uid='set_default_roles', sender=User)
def set_default_roles(sender, instance, **kwargs):

    if kwargs.get('created', False):
        for default_role in DEFAULT_ROLES:
            try:
                role = Role.objects.get(name=default_role)
                role.add_member(instance)
            except ObjectDoesNotExist:
                pass
