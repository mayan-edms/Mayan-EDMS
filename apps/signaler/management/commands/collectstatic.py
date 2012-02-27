from django.contrib.staticfiles.management.commands import collectstatic

from signaler.signals import pre_collectstatic


class Command(collectstatic.Command):
    """
    Wrapper for the collectstatic command
    """

    def handle_noargs(self, *args, **kwargs):
        pre_collectstatic.send(sender=self)
        super(Command, self).handle_noargs(*args, **kwargs)
