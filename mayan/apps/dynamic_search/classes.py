from collections import Iterable
import functools
import logging

from django.apps import apps
from django.contrib.admin.utils import (
    get_fields_from_path, reverse_field_path
)
from django.db import models
from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.exceptions import ResolverPipelineError
from mayan.apps.common.utils import (
    ResolverPipelineModelAttribute, get_class_full_name
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
    def get_instance(extra_kwargs=None):
        kwargs = setting_backend_arguments.value.copy()
        if extra_kwargs:
            kwargs.update(extra_kwargs)

        return import_string(dotted_path=setting_backend.value)(
            **kwargs
        )

    @staticmethod
    def limit_queryset(queryset):
        pk_list = queryset.values('pk')[:setting_results_limit.value]
        return queryset.filter(pk__in=pk_list)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def _search(self, global_and_search, query, search_model, user):
        raise NotImplementedError

    def cleanup_query(self, query, search_model):
        search_field_names = [
            search_field.get_full_name() for search_field in search_model.search_fields
        ]

        clean_query = {}

        if 'q' in query:
            value = query['q']
            if value:
                clean_query = {key: value for key in search_field_names}
        else:
            # Allow only valid search fields for the search model and scoping keys.
            clean_query = {
                key: value for key, value in query.items() if key in search_field_names and value
            }

        return clean_query

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
        else:
            # If query if empty, create an empty scope 0.
            scopes.setdefault(DEFAULT_SCOPE_ID, {})
            scopes[DEFAULT_SCOPE_ID].setdefault('match_all', scope_match_all)
            scopes[DEFAULT_SCOPE_ID].setdefault('query', {})

        return {
            'operators': operators, 'result_scope': result_scope,
            'scopes': scopes
        }

    def deindex_instance(self, instance):
        raise NotImplementedError

    def index_instance(self, instance):
        raise NotImplementedError

    def search(
        self, query, search_model, user, global_and_search=False
    ):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        result = self.decode_query(
            global_and_search=global_and_search, query=query
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
                query = self.cleanup_query(
                    query=scope['query'], search_model=search_model
                )
            except KeyError:
                raise DynamicSearchException(
                    'Scope `{}` does not specify a query.'.format(result_scope)
                )
            else:
                if query:
                    return self._search(
                        global_and_search=scope['match_all'],
                        ignore_limit=ignore_limit, search_model=search_model,
                        query=query, user=user
                    )
                else:
                    return search_model.model._meta.default_manager.none()


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
        return get_fields_from_path(model=self.get_model(), path=self.field)[-1]

    def uses_many_to_many_field(self):
        try:
            local_field_name, related_field_name = self.field.split('__', 1)
        except ValueError:
            local_field_name = self.field

        field = self.get_models()._meta.get_field(field_name=local_field_name)
        return isinstance(field, models.fields.related.ManyToManyField)

    @property
    def label(self):
        return self._label or self.get_model_field().verbose_name

    @cached_property
    def model(self):
        return self.search_model.model


class SearchModel(AppsModuleLoaderMixin):
    _loader_module_name = 'search'
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
                    if item is not None:
                        yield item
                    else:
                        yield ''

    @staticmethod
    def function_return_same(value):
        return value

    @staticmethod
    def initialize():
        # Hide a circular import.
        from .handlers import (
            handler_index_instance,
            handler_index_instance_m2m,
            handler_factory_deindex_instance,
            handler_factory_index_related_instance_delete,
            handler_factory_index_related_instance_m2m,
            handler_factory_index_related_instance_save
        )

        for search_model in SearchModel.all():
            for field in search_model.search_fields:
                fields = get_fields_from_path(
                    model=search_model.model, path=field.field
                )
                field = fields[0]

                try:
                    through = field.remote_field.through
                except AttributeError:
                    pass
                else:
                    m2m_changed.connect(
                        dispatch_uid='search_handler_index_instance_m2m',
                        receiver=handler_index_instance_m2m,
                        sender=through,
                        weak=False
                    )

            post_save.connect(
                dispatch_uid='search_handler_index_instance',
                receiver=handler_index_instance, sender=search_model.model
            )
            pre_delete.connect(
                dispatch_uid='search_handler_deindex_instance_{}'.format(
                    get_class_full_name(klass=search_model.model)
                ),
                receiver=handler_factory_deindex_instance(
                    search_model=search_model
                ),
                sender=search_model.model, weak=False
            )

            for related_model, path in search_model.get_related_models():
                post_save.connect(
                    dispatch_uid='search_handler_index_related_instance_{}_{}'.format(
                        get_class_full_name(klass=search_model.model),
                        get_class_full_name(klass=related_model)
                    ),
                    receiver=handler_factory_index_related_instance_save(
                        reverse_field_path=path
                    ), sender=related_model, weak=False
                )
                pre_delete.connect(
                    dispatch_uid='search_handler_index_related_instance_delete_{}_{}'.format(
                        get_class_full_name(klass=search_model.model),
                        get_class_full_name(klass=related_model)
                    ),
                    receiver=handler_factory_index_related_instance_delete(
                        reverse_field_path=path
                    ), sender=related_model, weak=False
                )

                many_to_many_field = get_fields_from_path(
                    model=related_model, path=path
                )[0]
                try:
                    through = many_to_many_field.through
                except AttributeError:
                    """Non fatal."""
                else:
                    # Since we are using the through model, remove the first
                    # entry of the path as it references the through model
                    # itself.
                    path_parts = path.split('__')

                    new_path = '__'.join(path_parts[1:])

                    if not new_path:
                        new_path = path

                    m2m_changed.connect(
                        dispatch_uid='search_handler_index_related_instance_m2m_{}_{}'.format(
                            get_class_full_name(klass=search_model.model),
                            get_class_full_name(klass=related_model)
                        ),
                        receiver=handler_factory_index_related_instance_m2m(
                            reverse_field_path=new_path
                        ),
                        sender=through,
                        weak=False
                    )

    @classmethod
    def all(cls):
        return sorted(
            list(set(cls._registry.values())), key=lambda x: x.label
        )

    @classmethod
    def as_choices(cls):
        return cls._registry

    @classmethod
    @functools.lru_cache(maxsize=None)
    def get(cls, name):
        try:
            result = cls._registry[name]
        except KeyError:
            raise KeyError(_('Unknown search model `%s`.') % name)
        else:
            #if not hasattr(result, 'serializer'):
            if getattr(result, 'serializer_path', None):
                result.serializer = import_string(
                    dotted_path=result.serializer_path
                )

        return result

    @classmethod
    def get_default(cls):
        for search_class in cls.all():
            if search_class.default:
                return search_class

    @classmethod
    def get_for_model(cls, instance):
        # Works the same for model classes and model instances.
        return cls.get(name=instance._meta.label)

    def __init__(
        self, app_label, model_name, default=False, label=None,
        list_mode=None, manager_name=None, permission=None,
        queryset=None, serializer_path=None
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

        self.manager_name = manager_name or self.model._meta.default_manager.name

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
            return self.model._meta.managers_map[self.manager_name].all()

    def get_related_models(self):
        result = set()
        for search_field in self.search_fields:
            obj, path = reverse_field_path(
                model=self.model, path=search_field.field
            )
            if path:
                # Ignore search model fields.
                result.add((obj, path))

        return result

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

    def uses_many_to_many_fields(self):
        return any(
            [
                search_field.uses_many_to_many_field for search_field in self.search_fields
            ]
        )

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

    def populate(self, field_map, instance):
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
                        value = ' '.join(value)
                except TypeError:
                    """Value is not a list."""
            except ResolverPipelineError:
                """Not fatal."""
            else:
                result[field] = field_map[field].get(
                    'transformation', SearchModel.function_return_same
                )(value)

        return result
