from colorful.fields import RGBColorField
import elasticsearch_dsl
import whoosh
from whoosh import qparser  # NOQA Used to initialize the whoosh.fields module.

from django.db import models

QUERY_OPERATION_AND = 1
QUERY_OPERATION_OR = 2
TERM_OPERATION_AND = 'AND'
TERM_OPERATION_OR = 'OR'
TERM_OPERATIONS = [TERM_OPERATION_AND, TERM_OPERATION_OR]
TERM_QUOTES = ['"', '\'']
TERM_NEGATION_CHARACTER = '-'
TERM_SPACE_CHARACTER = ' '

TEXT_LOCK_INSTANCE_DEINDEX = 'dynamic_search_deindex_instance'
TEXT_LOCK_INSTANCE_INDEX = 'dynamic_search_index_instance'

# Elastic search specific.
DJANGO_TO_ELASTIC_SEARCH_FIELD_MAP = {
    models.AutoField: {'field': elasticsearch_dsl.field.Keyword},
    models.BooleanField: {'field': elasticsearch_dsl.field.Keyword},
    models.CharField: {'field': elasticsearch_dsl.field.Text},
    models.EmailField: {'field': elasticsearch_dsl.field.Keyword},
    models.DateTimeField: {
        'field': elasticsearch_dsl.field.Keyword,
        'transformation': lambda value: value.isoformat()
    },
    models.TextField: {'field': elasticsearch_dsl.field.Text},
    models.UUIDField: {
        'field': elasticsearch_dsl.field.Keyword, 'transformation': str
    },
    RGBColorField: {'field': elasticsearch_dsl.field.Keyword},
}

# Whoosh specific.
DJANGO_TO_WHOOSH_FIELD_MAP = {
    models.AutoField: {
        'field': whoosh.fields.ID(stored=True, unique=True),
        'transformation': str
    },
    models.CharField: {'field': whoosh.fields.TEXT},
    models.DateTimeField: {
        'field': whoosh.fields.TEXT, 'transformation': str
    },
    models.EmailField: {'field': whoosh.fields.TEXT},
    models.TextField: {'field': whoosh.fields.TEXT},
    models.UUIDField: {'field': whoosh.fields.TEXT, 'transformation': str},
    RGBColorField: {'field': whoosh.fields.TEXT},
}

WHOOSH_INDEX_DIRECTORY_NAME = 'whoosh'
