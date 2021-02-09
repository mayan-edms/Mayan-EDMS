from django.core import management


def handler_pre_initial_setup(sender, **kwargs):
    management.call_command(command_name='migrate', interactive=False)


def handler_pre_upgrade(sender, **kwargs):
    management.call_command(
        command_name='migrate', fake_initial=True, interactive=False
    )
    management.call_command(command_name='purgeperiodictasks')
