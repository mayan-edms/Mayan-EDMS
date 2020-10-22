import logging

from django.apps import apps
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from mayan.apps.common.literals import LIST_MODE_CHOICE_LIST

logger = logging.getLogger(name=__name__)


class SearchBackend(object):
    def search(self, global_and_search, search_model, query_string, user):
        raise NotImplementedError


class SearchField(object):
    """
    Search for terms in fields that directly belong to the parent SearchModel
    """
    def __init__(self, search_model, field, label, transformation_function=None):
        self.search_model = search_model
        self.field = field
        self.label = label
        self.transformation_function = transformation_function

    def get_full_name(self):
        return self.field

    def get_model(self):
        return self.search_model.model


@python_2_unicode_compatible
class SearchModel(object):
    _registry = {}

    @classmethod
    def all(cls):
        return sorted(list(cls._registry.values()), key=lambda x: x.label)

    @classmethod
    def as_choices(cls):
        return cls._registry

    @classmethod
    def get(cls, name):
        try:
            result = cls._registry[name]
        except KeyError:
            raise KeyError(_('No search model matching the query'))
        if not hasattr(result, 'serializer'):
            result.serializer = import_string(dotted_path=result.serializer_path)

        return result

    def __init__(
        self, app_label, model_name, serializer_path, label=None,
        list_mode=None, permission=None, queryset=None
    ):
        self.app_label = app_label
        self.list_mode = list_mode or LIST_MODE_CHOICE_LIST
        self.model_name = model_name
        self.search_fields = []
        self._model = None  # Lazy
        self._label = label
        self.serializer_path = serializer_path
        self.permission = permission
        self.queryset = queryset
        self.__class__._registry[self.get_full_name()] = self

    def __str__(self):
        return force_text(s=self.label)

    def add_model_field(self, *args, **kwargs):
        """
        Add a search field that directly belongs to the parent SearchModel
        """
        search_field = SearchField(self, *args, **kwargs)
        self.search_fields.append(search_field)

    def get_fields_simple_list(self):
        """
        Returns a list of the fields for the SearchModel
        """
        result = []
        for search_field in self.search_fields:
            result.append((search_field.get_full_name(), search_field.label))

        return result

    def get_full_name(self):
        return '%s.%s' % (self.app_label, self.model_name)

    def get_queryset(self):
        if self.queryset:
            return self.queryset()
        else:
            return self.model.objects.all()

    def get_search_field(self, full_name):
        try:
            return self.search_fields[full_name]
        except KeyError:
            raise KeyError('No search field named: %s' % full_name)

    @property
    def label(self):
        if not self._label:
            self._label = self.model._meta.verbose_name
        return self._label

    @property
    def model(self):
        if not self._model:
            self._model = apps.get_model(self.app_label, self.model_name)
        return self._model

    @property
    def pk(self):
        return self.get_full_name()
