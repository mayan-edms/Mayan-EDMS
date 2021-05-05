from collections import Iterable
import logging

from django.apps import apps
from django.db.models.signals import post_save, pre_delete
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.exceptions import ResolverPipelineError
from mayan.apps.common.utils import (
    ResolverPipelineModelAttribute, get_related_field
)
from mayan.apps.views.literals import LIST_MODE_CHOICE_LIST

from .exceptions import DynamicSearchException
from .literals import (
    DEFAULT_SCOPE_OPERATOR, DELIMITER, SCOPE_DELIMITER,
    SCOPE_OPERATOR_CHOICES
)
from .settings import (
    setting_backend, setting_backend_arguments,
    setting_results_limit
)
logger = logging.getLogger(name=__name__)


class SearchBackend:
    @staticmethod
    def get_instance():
        return import_string(dotted_path=setting_backend.value)(
            **setting_backend_arguments.value
        )

    @staticmethod
    def limit_queryset(queryset):
        pk_list = queryset.values('pk')[:setting_results_limit.value]
        return queryset.filter(pk__in=pk_list)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def _search(self, global_and_search, search_model, query_string, user):
        raise NotImplementedError

    def deindex_instance(self, instance):
        raise NotImplementedError

    def index_instance(self, instance):
        raise NotImplementedError

    def search(
        self, search_model, query_string, user, global_and_search=False
    ):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        # Clean up the query_string
        # The original query_string is immutable, create a new
        # mutable copy
        query_string = query_string.copy()
        query_string.pop('_match_all', None)

        # Turn scoped query dictionary into a series of unscoped queries.
        scopes = {}
        operators = []

        operator_marker = '{}operator'.format(SCOPE_DELIMITER)
        result_marker = '{}result'.format(SCOPE_DELIMITER)
        result = '0'

        unscoped_entry = False

        for key, value in query_string.items():
            # Check if the entry is a special operator key.
            if key.startswith(operator_marker):
                scope_sources = list(
                    key[len(operator_marker) + 1:].split(DELIMITER)
                )

                operator, result = value.split(DELIMITER)

                operators.append(
                    {
                        'scope_sources': scope_sources,
                        'function': SCOPE_OPERATOR_CHOICES[operator],
                        'result': result
                    }
                )
            elif key.startswith(result_marker):
                result = value
            else:
                # Detect scope markers. Example: __0 or __10 or __b.
                if key.startswith(SCOPE_DELIMITER):
                    # Scoped entry found.
                    scope_index, unscoped_key = key[len(SCOPE_DELIMITER):].split(DELIMITER, 1)
                else:
                    # Non scoped query entries are assigned to scope 0.
                    scope_index = '0'
                    unscoped_key = key
                    unscoped_entry = True

                scopes.setdefault(scope_index, {'query': {}})
                scopes[scope_index]['query'][unscoped_key] = value

        if unscoped_entry:
            operators.append(
                {
                    'scope_sources': ['0', '0'],
                    'function': SCOPE_OPERATOR_CHOICES[DEFAULT_SCOPE_OPERATOR],
                    'result': '0'
                }
            )

        # Recursive call to the backend's search using queries as unscoped
        # and then merge then using the corresponding operator.
        queryset = search_model.model._meta.default_manager.none()

        queryset = self.solve_scope(
            global_and_search=global_and_search, operators=operators,
            result=result, search_model=search_model, scopes=scopes,
            user=user
        )

        if search_model.permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=search_model.permission, queryset=queryset,
                user=user
            )

        return queryset

    def solve_scope(self, global_and_search, search_model, user, result, scopes, operators):
        queryset = search_model.model._meta.default_manager.none()

        for operator in operators:
            if result == operator['result']:

                for scope_index in operator['scope_sources']:
                    try:
                        query_string = scopes[scope_index]['query']
                    except KeyError:
                        raise DynamicSearchException(
                            'Scope `{}` not found.'.format(scope_index)
                        )

                    results = self._search(
                        global_and_search=global_and_search,
                        search_model=search_model, query_string=query_string,
                        user=user
                    )

                    if not queryset:
                        queryset = results
                    else:
                        queryset = operator['function'](queryset, results)

                return queryset

        raise DynamicSearchException(
            'Result scope `{}` not found.'.format(result)
        )


class SearchField:
    """
    Search for terms in fields that directly belong to the parent SearchModel
    """
    def __init__(
        self, search_model, field, label=None, transformation_function=None
    ):
        self.search_model = search_model
        self.field = field
        self._label = label
        self.transformation_function = transformation_function

    def get_full_name(self):
        return self.field

    def get_model(self):
        return self.search_model.model

    def get_model_field(self):
        return get_related_field(
            model=self.get_model(), related_field_name=self.field
        )

    @property
    def label(self):
        return self._label or self.get_model_field().verbose_name


class SearchModel(AppsModuleLoaderMixin):
    _loader_module_name = 'search'
    _model_search_relationships = {}
    _registry = {}

    @staticmethod
    def flatten_list(value):
        if isinstance(value, (str, bytes)):
            yield value
        else:
            for item in value:
                if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
                    yield from SearchModel.flatten_list(value=item)
                else:
                    yield item

    @staticmethod
    def function_return_same(value):
        return value

    @staticmethod
    def initialize():
        # Hide a circular import
        from .handlers import (
            handler_factory_deindex_instance, handler_index_instance
        )

        for search_model in SearchModel.all():
            post_save.connect(
                dispatch_uid='search_handler_index_instance_{}'.format(search_model),
                receiver=handler_index_instance,
                sender=search_model.model
            )
            pre_delete.connect(
                dispatch_uid='search_handler_deindex_instance_{}'.format(search_model),
                receiver=handler_factory_deindex_instance(search_model=search_model),
                sender=search_model.model,
                weak=False
            )
            for proxy in search_model.proxies:
                post_save.connect(
                    dispatch_uid='search_handler_index_instance_{}'.format(search_model),
                    receiver=handler_index_instance,
                    sender=proxy
                )
                pre_delete.connect(
                    dispatch_uid='search_handler_deindex_instance_{}'.format(search_model),
                    receiver=handler_factory_deindex_instance(search_model=search_model),
                    sender=proxy,
                    weak=False
                )

            search_model._initialize()

    @classmethod
    def all(cls):
        return sorted(
            list(set(cls._registry.values())), key=lambda x: x.label
        )

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

    @classmethod
    def get_default(cls):
        for search_class in cls.all():
            if search_class.default:
                return search_class

    @classmethod
    def get_for_model(cls, instance):
        return cls.get(name=instance._meta.label)

    def __init__(
        self, app_label, model_name, serializer_path, default=False,
        label=None, list_mode=None, permission=None, queryset=None
    ):
        self.default = default
        self._label = label
        self.app_label = app_label
        self.list_mode = list_mode or LIST_MODE_CHOICE_LIST
        self.model_name = model_name
        self._proxies = []  # Lazy
        self.permission = permission
        self.queryset = queryset
        self.search_fields = []
        self.serializer_path = serializer_path

        if default:
            for search_class in self.__class__._registry.values():
                search_class.default = False

        self.__class__._registry[self.get_full_name()] = self

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__, self.label
        )

    def __str__(self):
        return force_text(s=self.label)

    def _initialize(self):
        for search_field in self.search_fields:
            related_model = get_related_field(
                model=self.model, related_field_name=search_field.field
            ).model

            if related_model != self.model:
                self.__class__._model_search_relationships.setdefault(
                    self.model, set()
                )
                self.__class__._model_search_relationships[self.model].add(
                    related_model
                )

                self.__class__._model_search_relationships.setdefault(
                    related_model, set()
                )
                self.__class__._model_search_relationships[related_model].add(
                    self.model
                )

    def add_model_field(self, *args, **kwargs):
        """
        Add a search field that directly belongs to the parent SearchModel
        """
        search_field = SearchField(self, *args, **kwargs)
        self.search_fields.append(search_field)

    def add_proxy_model(self, app_label, model_name):
        self._proxies.append(
            {
                'app_label': app_label, 'model_name': model_name
            }
        )

        self.__class__._registry['{}.{}'.format(app_label, model_name)] = self

    def get_fields_simple_list(self):
        """
        Returns a list of the fields for the SearchModel
        """
        result = []
        for search_field in self.search_fields:
            result.append(
                (search_field.get_full_name(), search_field.label)
            )

        return sorted(result, key=lambda x: x[1])

    def get_full_name(self):
        return '{}.{}'.format(self.app_label, self.model_name)

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

    @cached_property
    def label(self):
        if not self._label:
            self._label = self.model._meta.verbose_name
        return self._label

    @cached_property
    def model(self):
        return apps.get_model(
            app_label=self.app_label, model_name=self.model_name
        )

    @cached_property
    def pk(self):
        return self.get_full_name()

    @cached_property
    def proxies(self):
        result = []
        for proxy in self._proxies:
            result.append(
                apps.get_model(
                    app_label=proxy['app_label'], model_name=proxy['model_name']
                )
            )
        return result

    def sieve(self, field_map, instance):
        """
        Method that receives an instance and a field map dictionary
        consisting of attribute names and transformations to apply.
        Returns a dictionary of the instance values with their respective
        transformations. Makes it easy to pre process an instance before
        indexing it.
        """
        result = {}
        for field in field_map:
            try:
                value = ResolverPipelineModelAttribute.resolve(
                    attribute=field, obj=instance
                )
                try:
                    value = list(SearchModel.flatten_list(value))
                    if value == [None]:
                        value = None
                    else:
                        value = ''.join(value)
                except TypeError:
                    """Value is not a list"""
            except ResolverPipelineError:
                """Not fatal"""
            else:
                result[field] = field_map[field].get(
                    'transformation', SearchModel.function_return_same
                )(value)

        return result
