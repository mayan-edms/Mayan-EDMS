from __future__ import unicode_literals

from django.apps import apps

from .events import event_user_logged_in, event_user_logged_out


def handler_initialize_new_user_options(sender, instance, **kwargs):
    UserOptions = apps.get_model(
        app_label='user_management', model_name='UserOptions'
    )

    if kwargs['created']:
        UserOptions.objects.create(user=instance)


def handler_user_logged_in(sender, **kwargs):
    event_user_logged_in.commit(
        actor=kwargs['user'], target=kwargs['user']
    )


def handler_user_logged_out(sender, **kwargs):
    event_user_logged_out.commit(
        actor=kwargs['user'], target=kwargs['user']
    )
