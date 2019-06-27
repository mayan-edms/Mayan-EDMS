from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model


def create_system_user():
    """
    User account without a password used to attach events that normally
    won't have an actor and a target
    """
    user, created = get_user_model().objects.get_or_create(
        username='system', defaults={
            'first_name': 'System', 'is_staff': False
        }
    )

    return user


def get_system_user():
    user = get_user_model().objects.get(username='system')

    return user
