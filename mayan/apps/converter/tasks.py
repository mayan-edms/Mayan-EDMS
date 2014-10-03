import logging

from mayan.celery import app

from .api import convert

logger = logging.getLogger(__name__)


@app.task
def task_convert(*args, **kwargs):
    return convert(*args, **kwargs)
