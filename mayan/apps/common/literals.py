from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

DELETE_STALE_UPLOADS_INTERVAL = 60 * 10  # 10 minutes
DJANGO_SQLITE_BACKEND = 'django.db.backends.sqlite3'
MAYAN_PYPI_NAME = 'mayan-edms'
MESSAGE_SQLITE_WARNING = _(
    'Your database backend is set to use SQLite. SQLite should only be used '
    'for development and testing, not for production.'
)
PYPI_URL = 'https://pypi.python.org/pypi'
TIME_DELTA_UNIT_DAYS = 'days'
TIME_DELTA_UNIT_HOURS = 'hours'
TIME_DELTA_UNIT_MINUTES = 'minutes'

TIME_DELTA_UNIT_CHOICES = (
    (TIME_DELTA_UNIT_DAYS, _('Days')),
    (TIME_DELTA_UNIT_HOURS, _('Hours')),
    (TIME_DELTA_UNIT_MINUTES, _('Minutes')),
)
UPLOAD_EXPIRATION_INTERVAL = 60 * 60 * 24 * 7  # 7 days
