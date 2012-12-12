from apscheduler.scheduler import Scheduler

_lockdown = False
scheduler = Scheduler()


def lockdown():
    global _lockdown
    _lockdown = True


if not _lockdown:
    scheduler.start()
