import logging
from pathlib import Path

import whoosh
from whoosh import qparser
from whoosh.filedb.filestore import FileStorage
from whoosh.index import EmptyIndexError

from django.conf import settings

from mayan.apps.lock_manager.backends.base import LockingBackend
from mayan.apps.lock_manager.exceptions import LockError

from ..classes import SearchBackend, SearchField, SearchModel
from ..settings import setting_results_limit

from .literals import DJANGO_TO_WHOOSH_FIELD_MAP, WHOOSH_INDEX_DIRECTORY_NAME
logger = logging.getLogger(name=__name__)


class WhooshSearchBackend(SearchBackend):
    _resolved_field_maps = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index_path = Path(
            self.kwargs.get(
                'index_path', Path(settings.MEDIA_ROOT, WHOOSH_INDEX_DIRECTORY_NAME)
            )
        )
        self.index_path.mkdir(exist_ok=True)

    def _search(
        self, query_string, search_model, user, global_and_search=False,
        ignore_limit=False
    ):
        index = self.get_index(search_model=search_model)

        id_list = []
        with index.searcher() as searcher:
            search_string = []

            if 'q' in query_string:
                # Emulate full field set search
                for search_field in self.get_search_model_fields(search_model=search_model):
                    search_string.append(
                        '{}:({})'.format(search_field.get_full_name(), query_string['q'])
                    )
            else:
                for key, value in query_string.items():
                    if value:
                        search_string.append(
                            '{}:({})'.format(key, value)
                        )

            global_logic_string = ' AND ' if global_and_search else ' OR '
            search_string = global_logic_string.join(search_string)

            logger.debug('search_string: %s', search_string)

            parser = qparser.QueryParser(
                fieldname='_', schema=index.schema
            )
            parser.remove_plugin_class(cls=qparser.WildcardPlugin)
            parser.add_plugin(pin=qparser.PrefixPlugin())
            query = parser.parse(text=search_string)

            if ignore_limit:
                limit = None
            else:
                limit = setting_results_limit.value

            results = searcher.search(q=query, limit=limit)

            logger.debug('results: %s', results)

            for result in results:
                id_list.append(result['id'])

        return search_model.get_queryset().filter(
            id__in=id_list
        ).distinct()

    def clear_search_model_index(self, search_model):
        index = self.get_index(search_model=search_model)

        # Clear the model index
        self.get_storage().create_index(
            index.schema, indexname=search_model.get_full_name()
        )

    def deindex_instance(self, instance):
        try:
            lock = LockingBackend.get_backend().acquire_lock(
                name='dynamic_search_whoosh_deindex_instance'
            )
        except LockError:
            raise
        else:
            try:
                search_model = SearchModel.get_for_model(instance=instance)
                index = self.get_index(search_model=search_model)

                writer = index.writer()
                writer.delete_by_term('id', str(instance.pk))
                writer.commit()
            finally:
                lock.release()

    def get_index(self, search_model):
        storage = self.get_storage()

        schema = self.get_search_model_schema(search_model=search_model)

        try:
            index = storage.open_index(
                indexname=search_model.get_full_name(), schema=schema
            )
        except EmptyIndexError:
            index = storage.create_index(
                indexname=search_model.get_full_name(), schema=schema
            )

        return index

    def get_resolved_field_map(self, search_model):
        if search_model not in self._resolved_field_maps:

            result = {}
            for search_field in self.get_search_model_fields(search_model=search_model):
                whoosh_field_type = DJANGO_TO_WHOOSH_FIELD_MAP.get(
                    search_field.get_model_field().__class__
                )
                if whoosh_field_type:
                    result[search_field.get_full_name()] = whoosh_field_type
                else:
                    logger.warning(
                        'unknown field type "%s" for model "%s"',
                        search_field.get_full_name(),
                        search_model.get_full_name()
                    )

            self._resolved_field_maps[search_model] = result

        return self._resolved_field_maps[search_model]

    def get_search_model_fields(self, search_model):
        result = search_model.search_fields.copy()
        result.append(
            SearchField(search_model=search_model, field='id', label='ID')
        )
        return result

    def get_search_model_schema(self, search_model):
        field_map = self.get_resolved_field_map(search_model=search_model)
        schema_kwargs = {key: value['field'] for key, value in field_map.items()}
        return whoosh.fields.Schema(**schema_kwargs)

    def get_storage(self):
        return FileStorage(path=self.index_path)

    def index_instance(self, instance, exclude_set=None):
        try:
            lock = LockingBackend.get_backend().acquire_lock(
                name='dynamic_search_whoosh_index_instance'
            )
        except LockError:
            raise
        else:
            try:
                # Use a private method to allow using a single lock for
                # all recursions.
                self._index_instance(
                    instance=instance, exclude_set=exclude_set
                )
            finally:
                lock.release()

    def _index_instance(self, instance, exclude_set=None):
        if not exclude_set:
            exclude_set = set()

        # Avoid infinite recursion.
        if instance in exclude_set:
            return

        exclude_set.add(instance)

        try:
            search_model = SearchModel.get_for_model(instance=instance)
        except KeyError:
            """
            A KeyError is not fatal. It means search is not configured
            for this instance but we still need to check if one of its
            field's related models are configure for search and need
            to be updated.
            """
        else:
            index = self.get_index(search_model=search_model)

            writer = index.writer()
            kwargs = search_model.sieve(
                field_map=self.get_resolved_field_map(search_model=search_model), instance=instance
            )
            writer.delete_by_term('id', str(instance.pk))
            try:
                writer.add_document(**kwargs)
                writer.commit()
            except Exception as exception:
                logger.error(
                    'Unexpected exception while indexing object id: %s, '
                    'search model: %s, index data: %s, raw data: %s, '
                    'field map: %s; %s', search_model.get_full_name(),
                    instance.pk, kwargs, instance.__dict__,
                    self.get_resolved_field_map(search_model=search_model),
                    exception, exc_info=True
                )
                raise

        for field_class in instance._meta.get_fields():
            # Only to recursive indexing for related models that are
            # known to have a search configuration.
            if field_class.related_model and field_class.related_model in SearchModel._model_search_relationships.get(instance._meta.model, ()):
                field_instance = getattr(instance, field_class.name, None)

                if field_instance:
                    try:
                        # Try as a many field.
                        results = field_instance.all()
                    except AttributeError:
                        # Try as a one to one field.
                        try:
                            results = [field_instance.get()]
                        except AttributeError:
                            # It is neither then it must be a
                            # foreign key.
                            results = [field_instance]

                    for instance in results:
                        self._index_instance(
                            instance=instance, exclude_set=exclude_set
                        )

    def index_search_model(self, search_model):
        index = self.get_index(search_model=search_model)

        # Clear the model index
        self.get_storage().create_index(
            index.schema, indexname=search_model.get_full_name()
        )

        for instance in search_model.model._meta.default_manager.all():
            self.index_instance(instance=instance)
