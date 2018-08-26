from __future__ import unicode_literals

from django.apps import apps


def handler_initialize_new_user_options(sender, instance, **kwargs):
    UserOptions = apps.get_model(
        app_label='user_management', model_name='UserOptions'
    )

    if kwargs['created']:
        UserOptions.objects.create(user=instance)
