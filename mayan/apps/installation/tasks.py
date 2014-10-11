import requests

from mayan.celery import app

from .models import Installation


@app.task
def task_details_submit(max_retries=None, rate_limit='1/m', ignore_result=True):
    try:
        details = Installation.objects.get()
        details.submit()
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exception:
        raise self.retry(exc=exception)
