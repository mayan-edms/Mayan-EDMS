from optparse import make_option

from haystack.management.commands import update_index

from signaler.signals import post_update_index, pre_update_index


class Command(update_index.Command):
    """
    Wrapper for the haystack's update_index command
    """
    option_list = update_index.Command.option_list + (
        make_option('--mayan_runtime', action='store_true', dest='mayan_runtime', default=False),
    )

    def handle(self, *args, **kwargs):
        mayan_runtime = kwargs.pop('mayan_runtime')
        pre_update_index.send(sender=self, mayan_runtime=mayan_runtime)
        super(Command, self).handle(*args, **kwargs)
        post_update_index.send(sender=self, mayan_runtime=mayan_runtime)
