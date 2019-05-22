from __future__ import unicode_literals

import logging

from django.apps import apps
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FieldEntry(object):
    _registry = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    def __init__(self, dotted_path, label):
        self.dotted_path = dotted_path
        self.label = label

        self.__class__._registry[self.dotted_path] = self



FieldEntry(dotted_path='django.forms.CharField', label='Character field')
