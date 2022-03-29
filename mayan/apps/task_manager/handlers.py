from .utils import purge_periodic_tasks


def handler_perform_upgrade(sender, **kwargs):
    purge_periodic_tasks()
