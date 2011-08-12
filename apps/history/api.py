import pickle
import json

try:
    from psycopg2 import OperationalError
except ImportError:
    class OperationalError(Exception):
        pass

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.utils import DatabaseError
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.db import models

from history.models import HistoryType, History
from history.runtime_data import history_types_dict


@transaction.commit_manually
def register_history_type(history_type_dict):
    namespace = history_type_dict['namespace']
    name = history_type_dict['name']
    try:
        # Permanent
        history_type_obj, created = HistoryType.objects.get_or_create(
            namespace=namespace, name=name)
        history_type_obj.save()

        # Runtime
        history_types_dict.setdefault(namespace, {})
        history_types_dict[namespace][name] = {
            'label': history_type_dict['label'],
            'summary': history_type_dict.get('summary', u''),
            'details': history_type_dict.get('details', u''),
            'expressions': history_type_dict.get('expressions', []),
        }
    except DatabaseError:
        transaction.rollback()
        # Special case for ./manage.py syncdb
    except (OperationalError, ImproperlyConfigured):
        transaction.rollback()
        # Special for DjangoZoom, which executes collectstatic media
        # doing syncdb and creating the database tables
    else:
        transaction.commit()


def create_history(history_type_dict, source_object=None, data=None):
    history_type = get_object_or_404(HistoryType, namespace=history_type_dict['namespace'], name=history_type_dict['name'])
    new_history = History(history_type=history_type)
    if source_object:
        new_history.content_object = source_object
    if data:
        new_dict = {}
        for key, value in data.items():
            new_dict[key] = {}
            if isinstance(value, models.Model):
                new_dict[key]['value'] = serializers.serialize('json', [value])
            elif isinstance(value, models.query.QuerySet):
                new_dict[key]['value'] = serializers.serialize('json', value)
            else:
                new_dict[key]['value'] = json.dumps(value)
            new_dict[key]['type'] = pickle.dumps(type(value))

        new_history.dictionary = json.dumps(new_dict)
    new_history.save()
