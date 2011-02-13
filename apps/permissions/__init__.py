from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

from permissions.conf.settings import DEFAULT_ROLES

from models import Role


def user_post_save(sender, instance, **kwargs):
    for default_role in DEFAULT_ROLES:
        if isinstance(default_role, Role):
            default_role.add_member(instance)
        else:
            try:
                role = Role.objects.get(name=default_role)
                role.add_member(instance)
            except ObjectDoesNotExist:
                pass

post_save.connect(user_post_save, sender=User)
