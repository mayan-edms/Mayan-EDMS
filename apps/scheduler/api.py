from __future__ import absolute_import

from functools import wraps

from django import db

from .exceptions import AlreadyScheduled
from .runtime import scheduler

registered_jobs = {}


def close_connections(func):
    """
    Wrapper that closes all db connection before and after execution of
    its wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # This ensures the task gets a fresh db connection
        db.close_connection()
        result = func(*args, **kwargs)
        # This ensures no open connections remain after the task finishes executing
        db.close_connection()
        return result

    return wrapper


def register_interval_job(name, title, func, weeks=0, days=0, hours=0, minutes=0,
                         seconds=0, start_date=None, args=None,
                         kwargs=None, job_name=None, **options):

    if name in registered_jobs:
        raise AlreadyScheduled

    # Wrap the user function before adding it to the scheduler
    job = scheduler.add_interval_job(func=close_connections(func), weeks=weeks, days=days,
        hours=hours, minutes=minutes, seconds=seconds,
        start_date=start_date, args=args, kwargs=kwargs, **options)

    registered_jobs[name] = {'title': title, 'job': job}


def remove_job(name):
    if name in registered_jobs:
        scheduler.unschedule_job(registered_jobs[name]['job'])
        registered_jobs.pop(name)


def get_job_list():
    return registered_jobs.values()
