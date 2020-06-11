from django.utils.translation import ugettext_lazy as _

DEFAULT_COMMON_HOME_VIEW = 'common:home'
DJANGO_SQLITE_BACKEND = 'django.db.backends.sqlite3'

LOGGING_HANDLER_OPTIONS = ('console', 'logfile')

MESSAGE_DEPRECATION_WARNING = _(
    'This feature has been deprecated and will be removed in a future version.'
)
MESSAGE_SQLITE_WARNING = _(
    'Your database backend is set to use SQLite. SQLite should only be used '
    'for development and testing, not for production.'
)

TIME_DELTA_UNIT_DAYS = 'days'
TIME_DELTA_UNIT_HOURS = 'hours'
TIME_DELTA_UNIT_MINUTES = 'minutes'

TIME_DELTA_UNIT_CHOICES = (
    (TIME_DELTA_UNIT_DAYS, _('Days')),
    (TIME_DELTA_UNIT_HOURS, _('Hours')),
    (TIME_DELTA_UNIT_MINUTES, _('Minutes')),
)
