from django.utils.translation import ugettext_lazy as _

DJANGO_SQLITE_BACKEND = 'django.db.backends.sqlite3'

IMPORT_ERROR_EXCLUSION_TEXTS = (
    'doesn\'t look like a module path', 'No module named'
)

MESSAGE_SQLITE_WARNING = _(
    'Your database backend is set to use SQLite. SQLite should only be used '
    'for development and testing, not for production.'
)
