import logging
from optparse import make_option

from haystack.management.commands import update_index

from signaler.signals import post_update_index, pre_update_index

logger = logging.getLogger(__name__)

MAYAN_RUNTIME = 'mayan_runtime'
MAYAN_RUNTIME_OPT = '--%s' % MAYAN_RUNTIME


class Command(update_index.Command):
    """
    Wrapper for the haystack's update_index command
    """
    option_list = update_index.Command.option_list + (
        make_option(None, MAYAN_RUNTIME_OPT, action='store_true', dest=MAYAN_RUNTIME, default=False),
    )

    def handle(self, *args, **kwargs):
        mayan_runtime = kwargs.pop(MAYAN_RUNTIME)
        args = list(args)
        if MAYAN_RUNTIME_OPT in args:
            # Being called from another app
            mayan_runtime = True
            args.remove(MAYAN_RUNTIME_OPT)
        logger.debug('mayan_runtime: %s' % mayan_runtime)
        pre_update_index.send(sender=self, mayan_runtime=mayan_runtime)
        super(Command, self).handle(*args, **kwargs)
        post_update_index.send(sender=self, mayan_runtime=mayan_runtime)
