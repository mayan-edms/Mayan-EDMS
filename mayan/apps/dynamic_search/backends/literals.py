from colorful.fields import RGBColorField

import whoosh
from whoosh import qparser  # NOQA Used to initialize the whoosh.fields module

from django.db import models

QUERY_OPERATION_AND = 1
QUERY_OPERATION_OR = 2
TERM_OPERATION_AND = 'AND'
TERM_OPERATION_OR = 'OR'
TERM_OPERATIONS = [TERM_OPERATION_AND, TERM_OPERATION_OR]
TERM_QUOTES = ['"', '\'']
TERM_NEGATION_CHARACTER = '-'
TERM_SPACE_CHARACTER = ' '

DJANGO_TO_WHOOSH_FIELD_MAP = {
    models.AutoField: {
        'field': whoosh.fields.ID(stored=True), 'transformation': str
    },
    models.CharField: {'field': whoosh.fields.TEXT},
    models.EmailField: {'field': whoosh.fields.TEXT},
    models.TextField: {'field': whoosh.fields.TEXT},
    models.UUIDField: {'field': whoosh.fields.TEXT, 'transformation': str},
    RGBColorField: {'field': whoosh.fields.TEXT},
}
WHOOSH_INDEX_DIRECTORY_NAME = 'whoosh'
