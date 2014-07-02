import os

from django.conf import settings


FORM_SUBMIT_URL = 'https://docs.google.com/spreadsheet/formResponse'
FORM_KEY = 'dGZrYkw3SDl5OENMTG15emp1UFFEUWc6MQ'
FORM_RECEIVER_FIELD = 'entry.0.single'
TIMEOUT = 5
FABFILE_MARKER = os.path.join(settings.BASE_DIR, 'fabfile_install')
