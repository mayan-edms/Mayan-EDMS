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
    DEFAULT_SCOPE_ID, DELIMITER, SCOPE_MATCH_ALL, SCOPE_MARKER,
    SCOPE_OPERATOR_CHOICES, SCOPE_OPERATOR_MARKER, SCOPE_RESULT_MAKER
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
        self, search_model, query, user, global_and_search=False
    ):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        result = self.decode_query(
            query=query, global_and_search=global_and_search
        )

        # Recursive call to the backend's search using queries as unscoped
        # and then merge then using the corresponding operator.
        queryset = self.solve_scope(
            operators=result['operators'],
            result_scope=result['result_scope'], search_model=search_model,
            scopes=result['scopes'], user=user
        )

        if search_model.permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=search_model.permission, queryset=queryset,
                user=user
            )

        return SearchBackend.limit_queryset(queryset=queryset)

    def decode_query(self, query, global_and_search=False):
        # Clean up the query.
        # The original query is immutable, create a new
        # mutable copy.
        query.pop('_match_all', None)

        # Turn scoped query dictionary into a series of unscoped queries.
        operators = {}
        result_scope = DEFAULT_SCOPE_ID
        scope_match_all = False
        scopes = {}

        for key, value in query.items():
            scope_id = DEFAULT_SCOPE_ID

            # Check if the entry has a scope marker.
            if key.startswith(SCOPE_MARKER):
                # Remove the scope marker.
                key = key[len(SCOPE_MARKER):]

                if key.startswith(SCOPE_OPERATOR_MARKER):
                    # Check for operator.
                    # __operator_SCOPE_SCOPE=OPERATOR_SCOPE
                    key = key[len(SCOPE_OPERATOR_MARKER):]
                    operator_scopes = key[len(DELIMITER):].split(DELIMITER)
                    operator_text, result = value.split(DELIMITER)

                    operators[result] = {
                        'scopes': operator_scopes,
                        'function': SCOPE_OPERATOR_CHOICES[operator_text],
                    }
                elif key.startswith(SCOPE_RESULT_MAKER):
                    # Check for result.
                    # __result=SCOPE
                    result_scope = value
                else:
                    # Check scope match all.
                    # __SCOPE_match_all
                    if key.endswith(SCOPE_MATCH_ALL):
                        scope_id, key = key.split(DELIMITER, 1)
                        scopes.setdefault(scope_id, {})
                        scope_match_all = value.upper() == 'TRUE'
                        scopes[scope_id]['match_all'] = scope_match_all
                    else:
                        # Must be a scoped query.
                        # __SCOPE_QUERY=VALUE
                        scope_id, key = key.split(DELIMITER, 1)
                        scopes.setdefault(scope_id, {})
                        scopes[scope_id].setdefault('match_all', False)
                        scopes[scope_id].setdefault('query', {})

                        scopes[scope_id]['query'][key] = value
            else:
                scopes.setdefault(scope_id, {})
                scopes[scope_id].setdefault('match_all', scope_match_all)
                scopes[scope_id].setdefault('query', {})
                scopes[scope_id]['query'][key] = value

        return {
            'operators': operators, 'result_scope': result_scope,
            'scopes': scopes
        }

    def solve_scope(
        self, search_model, user, result_scope, scopes, operators
    ):
        if len(scopes) > 1:
            ignore_limit = True
        else:
            ignore_limit = False

        try:
            # Try scopes.
            scope = scopes[result_scope]
        except KeyError:
            try:
                # Try operators.
                operator = operators[result_scope]
            except KeyError:
                raise DynamicSearchException(
                    'Scope `{}` not found.'.format(result_scope)
                )
            else:
                result = None
                for scope in operator['scopes']:
                    queryset = self.solve_scope(
                        operators=operators, result_scope=scope,
                        search_model=search_model, scopes=scopes, user=user
                    )

                    if result is None:
                        result = queryset
                    else:
                        result = operator['function'](result, queryset)

                return result
        else:
            try:
                query_string = scope['query']
            except KeyError:
                raise DynamicSearchException(
                    'Scope `{}` does not specify a query.'.format(result_scope)
                )
            else:
                return self._search(
                    global_and_search=scope['match_all'],
                    ignore_limit=ignore_limit, search_model=search_model,
                    query_string=query_string, user=user
                )


class SearchField:
    """
    Search for terms in fields that directly belong to the parent
    SearchModel.
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
        # Hide a circular import.
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
        Add a search field that directly belongs to the parent SearchModel.
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
        Returns a list of the fields for the SearchModel.
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
                    """Value is not a list."""
            except ResolverPipelineError:
                """Not fatal."""
            else:
                result[field] = field_map[field].get(
                    'transformation', SearchModel.function_return_same
                )(value)

        return result
