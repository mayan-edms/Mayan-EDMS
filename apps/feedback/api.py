import requests

from django.utils.simplejson import dumps

FORM_SUBMIT_URL = 'https://docs.google.com/spreadsheet/formResponse'
FORM_KEY = 'dGZrYkw3SDl5OENMTG15emp1UFFEUWc6MQ'
FORM_RECEIVER_FIELD = 'entry.0.single'
TIMEOUT = 10


def submit_form(form):
    r = requests.post(FORM_SUBMIT_URL, data={'formkey': FORM_KEY, FORM_RECEIVER_FIELD: dumps(form.cleaned_data)}, timeout=TIMEOUT)
