from __future__ import absolute_import

from .runtime import scheduler
from .exceptions import AlreadyScheduled

registered_jobs = {}


def register_interval_job(name, title, func, weeks=0, days=0, hours=0, minutes=0,
                         seconds=0, start_date=None, args=None,
                         kwargs=None, job_name=None, **options):

    if name in registered_jobs:
        raise AlreadyScheduled

    job = scheduler.add_interval_job(func=func, weeks=weeks, days=days,
        hours=hours, minutes=minutes, seconds=seconds,
        start_date=start_date, args=args, kwargs=kwargs, **options)

    registered_jobs[name] = {'title': title, 'job': job}
    

def remove_job(name):
    if name in registered_jobs:
        scheduler.unschedule_job(registered_jobs[name]['job'])
        registered_jobs.pop(name)
        

def get_job_list():
    return registered_jobs.values()
