from haystack.management.commands import update_index

from signaler.signals import post_update_index, pre_update_index


class Command(update_index.Command):
    """
    Wrapper for the haystack's update_index command
    """

    def handle(self, *args, **kwargs):
        pre_update_index.send(sender=self)
        super(Command, self).handle(*args, **kwargs)
        post_update_index.send(sender=self)
