from celery.decorators import task, periodic_task
from celery.task.control import inspect

from job_processor.conf.settings import BACKEND


@task
def celery_task(func, *args, **kwargs):
    return func(*args, **kwargs)


def process_job(func, *args, **kwargs):
    if BACKEND == 'celery':
        return celery_task.delay(func, *args, **kwargs)
    elif BACKEND is None:
        return func(*args, **kwargs)
