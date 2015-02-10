from __future__ import unicode_literals

import requests

from mayan.celery import app

from .exceptions import AlreadyRegistered
from .models import RegistrationSingleton


# TODO: move rate_limit to literals.py
@app.task(bind=True, ignore_result=True, max_retries=None, rate_limit='1/m', throws=(AlreadyRegistered,))
def task_registration_register(self, form_data):
    try:
        RegistrationSingleton.register(form_data)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exception:
        raise self.retry(exc=exception)
