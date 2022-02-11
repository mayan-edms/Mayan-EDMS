import logging

from django.apps import apps
from django.contrib.admin.utils import (
    get_fields_from_path, reverse_field_path
)
from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.utils import get_class_full_name
from mayan.apps.views.literals import LIST_MODE_CHOICE_LIST

from .exceptions import DynamicSearchException
from .literals import (
    DEFAULT_SCOPE_ID, DELIMITER, MESSAGE_FEATURE_NO_STATUS, SCOPE_MATCH_ALL,
    SCOPE_MARKER, SCOPE_OPERATOR_CHOICES, SCOPE_OPERATOR_MARKER,
    SCOPE_RESULT_MAKER
)
from .settings import (
    setting_backend, setting_backend_arguments,
    setting_results_limit
)
logger = logging.getLogger(name=__name__)


class SearchBackend:
    _initialized = False
    _search_field_transformations = {}

    @staticmethod
    def _disable():
        for search_model in SearchModel.all():
            post_save.disconnect(
                dispatch_uid='search_handler_index_instance',
                sender=search_model.model
            )
            pre_delete.disconnect(
                dispatch_uid='search_handler_deindex_instance',
                sender=search_model.model
            )

            for proxy in search_model.proxies:
                post_save.disconnect(
                    dispatch_uid='search_handler_index_instance',
                    sender=proxy
                )
                pre_delete.disconnect(
                    dispatch_uid='search_handler_deindex_instance',
                    sender=proxy
                )

            for related_model, path in search_model.get_related_models():
                post_save.disconnect(
                    dispatch_uid='search_handler_index_related_instance_{}_{}'.format(
                        get_class_full_name(klass=search_model.model),
                        get_class_full_name(klass=related_model)
                    ), sender=related_model
                )
                pre_delete.disconnect(
                    dispatch_uid='search_handler_index_related_instance_delete_{}_{}'.format(
                        get_class_full_name(klass=search_model.model),
                        get_class_full_name(klass=related_model)
                    ), sender=related_model
                )

        for through_model, data in SearchModel.get_through_models().items():
            m2m_changed.disconnect(
                dispatch_uid='search_handler_index_related_instance_m2m_{}'.format(
                    get_class_full_name(klass=through_model),
                ), sender=through_model
            )

    @staticmethod
    def _enable():
        # Hidden import.
        from .handlers import (
            handler_deindex_instance, handler_index_instance,
            handler_factory_index_related_instance_delete,
            handler_factory_index_related_instance_m2m,
            handler_factory_index_related_instance_save
        )

        for search_model in SearchModel.all():
            post_save.connect(
                dispatch_uid='search_handler_index_instance',
                receiver=handler_index_instance, sender=search_model.model
            )
            pre_delete.connect(
                dispatch_uid='search_handler_deindex_instance',
                receiver=handler_deindex_instance,
                sender=search_model.model, weak=False
            )

            for proxy in search_model.proxies:
                post_save.connect(
                    dispatch_uid='search_handler_index_instance',
                    receiver=handler_index_instance, sender=proxy
                )
                pre_delete.connect(
                    dispatch_uid='search_handler_deindex_instance',
                    receiver=handler_deindex_instance,
                    sender=proxy, weak=False
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

        for through_model, data in SearchModel.get_through_models().items():
            m2m_changed.connect(
                dispatch_uid='search_handler_index_related_instance_m2m_{}'.format(
                    get_class_full_name(klass=through_model),
                ),
                receiver=handler_factory_index_related_instance_m2m(
                    data=data,
                ),
                sender=through_model, weak=False
            )

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

    def _search(self, global_and_search, query, search_model, user, ignore_limit):
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

    def close(self):
        """
        Optional method to terminate a backend instance, such as closing
        connections.
        """

    def decode_query(self, query, global_and_search=False):
        # Clean up the query.
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
                        scope_match_all = value.lower() in ['on', 'true']
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
                scopes[scope_id].setdefault('match_all', global_and_search)
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
        """
        Optional method to remove an model instance from the search index.
        """

    def get_resolved_field_map(self, search_model):
        result = {}
        for search_field in self.get_search_model_fields(search_model=search_model):
            backend_field_type = self.field_map.get(
                search_field.field_type
            )

            if backend_field_type:
                result[search_field.get_full_name()] = backend_field_type
            else:
                logger.warning(
                    'Unknown field type "%s" for model "%s"',
                    search_field.get_full_name(),
                    search_model.get_full_name()
                )

        return result

    def get_search_field_transformation(self, search_field):
        if search_field not in self.__class__._search_field_transformations:
            field_map = self.get_resolved_field_map(
                search_model=search_field.search_model
            )
            transformation = field_map[search_field.field].get(
                'transformation', SearchModel.function_return_same
            )
            self.__class__._search_field_transformations[
                search_field
            ] = transformation

        return self.__class__._search_field_transformations[search_field]

    def get_search_model_fields(self, search_model):
        result = search_model.search_fields.copy()
        result.append(
            SearchField(search_model=search_model, field='id', label='ID')
        )
        return result

    def get_status(self):
        """
        Backend specific method to provide status and statistics information.
        """
        if not hasattr(self, '_get_status'):
            return MESSAGE_FEATURE_NO_STATUS
        else:
            return self._get_status()

    def index_instance(self, instance, exclude_model=None, exclude_kwargs=None):
        """
        Optional method to add or update an model instance to the search
        index.
        """

    def index_search_model(self, search_model, range_string=None):
        """
        Optional method to add or update all instance of a model.
        """

    def initialize(self):
        if not self.__class__._initialized:
            self.__class__._initialized = True
            self._initialize()

    def _initialize(self):
        """
        Optional method to setup the backend. Executed once on every boot up.
        """

    def reset(self, search_model=None):
        """
        Optional method to clear all search indices.
        """

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
                    return search_model.get_queryset().none()

    def tear_down(self):
        """
        Optional method to clean up and/or destroy search backend structures
        like indices.
        """

    def upgrade(self):
        """
        Optional method to upgrade the search backend persistent structures.
        """


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

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__, self.field
        )

    @cached_property
    def field_type(self):
        return self.get_model_field().__class__

    def get_full_name(self):
        return self.field

    def get_model(self):
        return self.search_model.model

    def get_model_field(self):
        return get_fields_from_path(model=self.get_model(), path=self.field)[-1]

    @property
    def label(self):
        return self._label or self.get_model_field().verbose_name

    @cached_property
    def model(self):
        return self.search_model.model

    @cached_property
    def related_model(self):
        return self.get_model_field().model

    @cached_property
    def reverse_path(self):
        return reverse_field_path(model=self.model, path=self.field)[1]


class SearchModel(AppsModuleLoaderMixin):
    _loader_module_name = 'search'
    _registry = {}

    @staticmethod
    def function_return_same(value):
        return value

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
            raise KeyError(_('Unknown search model `%s`.') % name)
        else:
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
        return cls.get(name=instance._meta.label.lower())

    @classmethod
    def get_through_models(cls):
        through_models = {}

        for search_model in cls.all():
            for related_model, related_path in search_model.get_related_models():
                # Check is each related model is connected to a many to many.
                for field in related_model._meta.get_fields():
                    if field.many_to_many:
                        try:
                            through_model = field.through
                        except AttributeError:
                            through_model = field.remote_field.through

                        through_models.setdefault(through_model, {})
                        through_models[through_model].setdefault(related_model, set())
                        through_models[through_model][related_model].add(related_path)

        return through_models

    def __init__(
        self, app_label, model_name, default=False, label=None,
        list_mode=None, manager_name=None, permission=None,
        queryset=None, serializer_path=None
    ):
        self.default = default
        self._label = label
        self.app_label = app_label
        self.list_mode = list_mode or LIST_MODE_CHOICE_LIST
        self.model_name = model_name.lower()
        self._proxies = []  # Lazy
        self.permission = permission
        self.queryset = queryset
        self.search_fields = []
        self.search_fields_dict = {}
        self.serializer_path = serializer_path

        self.add_model_field(field='id', label=_('ID'))

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
        self.search_fields_dict[search_field.get_full_name()] = search_field

    def add_proxy_model(self, app_label, model_name):
        model_name = model_name.lower()
        self._proxies.append(
            {
                'app_label': app_label, 'model_name': model_name
            }
        )

        self.__class__._registry['{}.{}'.format(app_label, model_name)] = self

    @cached_property
    def fields_direct(self):
        result = []

        for search_field in self.search_fields:
            field_name = search_field.field

            if '__' not in field_name:
                result.append(search_field)

        return result

    @cached_property
    def fields_related(self):
        result = []

        for search_field in self.search_fields:
            field_name = search_field.field

            if '__' in field_name:
                result.append(search_field)

        return result

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
        if self.queryset is not None:
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
            return self.search_fields_dict[full_name]
        except KeyError:
            raise KeyError('No search field named: %s' % full_name)

    @cached_property
    def label(self):
        if not self._label:
            self._label = self.model._meta.verbose_name
        return self._label

    @cached_property
    def base_model(self):
        return self.model._meta.proxy_for_model or self.model

    @cached_property
    def model(self):
        return apps.get_model(
            app_label=self.app_label, model_name=self.model_name
        )

    @cached_property
    def pk(self):
        return self.get_full_name()

    def populate(
        self, backend, instance, exclude_model=None, exclude_kwargs=None
    ):
        result = {}
        search_model = SearchModel.get_for_model(instance=instance)

        for direct_field in search_model.fields_direct:
            field_name = direct_field.field

            # Fetch the fields that produce a finite number of results.
            value = getattr(instance, field_name)

            result[field_name] = backend.get_search_field_transformation(
                search_field=direct_field
            )(value)

        for related_field in search_model.fields_related:
            # Fetch the fields that produce an undetermined number of
            # results.
            # This implementation is a balance between memory usage and
            # performance.
            # Attempting to fetch all of these fields at the same time using
            # joins creates a single query that kills the database and
            # causes the OOM to kill this method's process due to run away
            # memory usage.
            # This implementation is not infinitely scalable but has been
            # tested up to 500 pages per document version + 500 pages per
            # document file with an indexing chunk size of 25 for a total
            # of 25,000 page results per super call.
            field_name = related_field.field
            last_field = field_name.split('__')[-1]

            sub_queryset = related_field.related_model._meta.default_manager.filter(
                **{
                    '{}'.format(related_field.reverse_path): instance.pk
                }
            ).values_list(last_field, flat=True)

            if exclude_model and related_field.related_model == exclude_model:
                sub_queryset = sub_queryset.exclude(**exclude_kwargs)

            final_value = []
            for value in sub_queryset.distinct():
                final_value.append(
                    backend.get_search_field_transformation(
                        search_field=related_field
                    )(value) or ''
                )

            result[field_name] = ' '.join(final_value)

        return result

    @property
    def proxies(self):
        result = []
        for proxy in self._proxies:
            result.append(
                apps.get_model(
                    app_label=proxy['app_label'], model_name=proxy['model_name']
                )
            )
        return result
