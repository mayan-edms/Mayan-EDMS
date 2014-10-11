import requests

from mayan.celery import app

from .models import Installation


@app.task(bind=True, ignore_result=True, max_retries=None, rate_limit='1/m')
def task_details_submit(self):
    try:
        details = Installation.objects.get()
        details.submit()
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exception:
        raise self.retry(exc=exception)
