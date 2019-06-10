from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

DEFAULT_COMMON_HOME_VIEW = 'common:home'
DELETE_STALE_UPLOADS_INTERVAL = 60 * 10  # 10 minutes
DJANGO_SQLITE_BACKEND = 'django.db.backends.sqlite3'

LIST_MODE_CHOICE_LIST = 'list'
LIST_MODE_CHOICE_ITEM = 'item'

MESSAGE_DEPRECATION_WARNING = _(
    'This feature has been deprecated and will be removed in a future version.'
)
MESSAGE_SQLITE_WARNING = _(
    'Your database backend is set to use SQLite. SQLite should only be used '
    'for development and testing, not for production.'
)

PK_LIST_SEPARATOR = ','

TEXT_SORT_FIELD_PARAMETER = '_sort_field'
TEXT_SORT_FIELD_VARIABLE_NAME = 'sort_field'
TEXT_SORT_ORDER_CHOICE_ASCENDING = 'asc'
TEXT_SORT_ORDER_CHOICE_DESCENDING = 'desc'
TEXT_SORT_ORDER_PARAMETER = '_sort_order'
TEXT_SORT_ORDER_VARIABLE_NAME = 'sort_order'

TIME_DELTA_UNIT_DAYS = 'days'
TIME_DELTA_UNIT_HOURS = 'hours'
TIME_DELTA_UNIT_MINUTES = 'minutes'

TIME_DELTA_UNIT_CHOICES = (
    (TIME_DELTA_UNIT_DAYS, _('Days')),
    (TIME_DELTA_UNIT_HOURS, _('Hours')),
    (TIME_DELTA_UNIT_MINUTES, _('Minutes')),
)
UPLOAD_EXPIRATION_INTERVAL = 60 * 60 * 24 * 7  # 7 days
