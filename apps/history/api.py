from __future__ import absolute_import

import pickle
import json

from django.db import transaction
from django.core import serializers
from django.db import models
from django.db.utils import DatabaseError

from .models import HistoryType, History
from .runtime_data import history_types_dict


class EventNamespace(object):
    def __init__(self, name, label):
        self.name = name
        self.label = label


class Event(object):
    @transaction.commit_on_success
    def __init__(self, namespace, name, label, summary=None, details=None, expressions=None):
        self.namespace = namespace
        self.name = name
        self.label = label
        self.summary = summary or ''
        self.details = details or ''
        self.expressions = expressions or {}

        try:
            self.history_type_obj, created = HistoryType.objects.get_or_create(
                namespace=self.namespace.name, name=self.name)
            self.history_type_obj.save()
            history_types_dict.setdefault(self.namespace.name, {})
            history_types_dict[self.namespace.name][self.name] = self
        except DatabaseError:
            # Special case for syncdb
            transaction.rollback()

    def commit(self, source_object=None, data=None):
        new_history = History(history_type=self.history_type_obj)
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
