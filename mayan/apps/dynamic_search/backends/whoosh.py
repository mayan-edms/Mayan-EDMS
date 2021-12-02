import logging
from pathlib import Path

import whoosh
from whoosh import qparser
from whoosh.filedb.filestore import FileStorage
from whoosh.index import EmptyIndexError
from whoosh.query import Every

from django.conf import settings

from mayan.apps.common.utils import any_to_bool
from mayan.apps.lock_manager.backends.base import LockingBackend
from mayan.apps.lock_manager.exceptions import LockError

from ..classes import SearchBackend, SearchField, SearchModel
from ..exceptions import DynamicSearchRetry
from ..settings import setting_results_limit

from .literals import (
    DJANGO_TO_WHOOSH_FIELD_MAP, TEXT_LOCK_INSTANCE_DEINDEX,
    TEXT_LOCK_INSTANCE_INDEX, WHOOSH_INDEX_DIRECTORY_NAME,
)
logger = logging.getLogger(name=__name__)


class WhooshSearchBackend(SearchBackend):
    def __init__(self, **kwargs):
        index_path = kwargs.pop('index_path', None)
        writer_limitmb = kwargs.pop('writer_limitmb', 128)
        writer_multisegment = kwargs.pop('writer_multisegment', False)
        writer_procs = kwargs.pop('writer_procs', 1)

        super().__init__(**kwargs)

        self.index_path = Path(
            index_path or Path(settings.MEDIA_ROOT, WHOOSH_INDEX_DIRECTORY_NAME)
        )
        self.index_path.mkdir(exist_ok=True)

        if writer_limitmb:
            writer_limitmb = int(writer_limitmb)

        if writer_multisegment:
            writer_multisegment = any_to_bool(value=writer_multisegment)

        if writer_procs:
            writer_procs = int(writer_procs)

        self.writer_kwargs = {
            'limitmb': writer_limitmb, 'multisegment': writer_multisegment,
            'procs': writer_procs
        }

    def _search(
        self, query, search_model, user, global_and_search=False,
        ignore_limit=False
    ):
        index = self.get_or_create_index(search_model=search_model)

        id_list = []
        with index.searcher() as searcher:
            search_string = []

            for key, value in query.items():
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
            whoosh_query = parser.parse(text=search_string)

            if ignore_limit:
                limit = None
            else:
                limit = setting_results_limit.value

            results = searcher.search(q=whoosh_query, limit=limit)

            logger.debug('results: %s', results)

            for result in results:
                id_list.append(result['id'])

        return search_model.get_queryset().filter(
            id__in=id_list
        ).distinct()

    def clear_search_model_index(self, search_model):
        schema = self.get_search_model_schema(search_model=search_model)

        # Clear the model index.
        self.get_storage().create_index(
            indexname=search_model.get_full_name(), schema=schema
        )

    def deindex_instance(self, instance):
        try:
            lock = LockingBackend.get_backend().acquire_lock(
                name=TEXT_LOCK_INSTANCE_DEINDEX
            )
        except LockError:
            raise
        else:
            try:
                search_model = SearchModel.get_for_model(instance=instance)
                index = self.get_or_create_index(search_model=search_model)

                with index.writer(**self.writer_kwargs) as writer:
                    writer.delete_by_term('id', str(instance.pk))
            finally:
                lock.release()

    def get_or_create_index(self, search_model):
        storage = self.get_storage()
        schema = self.get_search_model_schema(search_model=search_model)

        try:
            # Explictly specify the schema. Allows using existing index
            # when the schema changes.
            index = storage.open_index(
                indexname=search_model.get_full_name(), schema=schema
            )
        except EmptyIndexError:
            index = storage.create_index(
                indexname=search_model.get_full_name(), schema=schema
            )

        return index

    def get_resolved_field_map(self, search_model):
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

        return result

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

    def get_status(self):
        result = []

        title = 'Whoosh search model indexing status'
        result.append(title)
        result.append(len(title) * '=')

        for search_model in SearchModel.all():
            index = self.get_or_create_index(search_model=search_model)
            search_results = index.searcher().search(Every('id'))

            result.append(
                '{}: {}'.format(
                    search_model.label, search_results.estimated_length()
                )
            )

        return result

    def get_storage(self):
        return FileStorage(path=self.index_path)

    def index_instance(self, instance, exclude_model=None, exclude_kwargs=None):
        try:
            lock = LockingBackend.get_backend().acquire_lock(
                name=TEXT_LOCK_INSTANCE_INDEX
            )
        except LockError:
            raise
        else:
            try:
                search_model = SearchModel.get_for_model(instance=instance)
                index = self.get_or_create_index(search_model=search_model)

                with index.writer(**self.writer_kwargs) as writer:
                    kwargs = search_model.populate(
                        field_map=self.get_resolved_field_map(
                            search_model=search_model
                        ), instance=instance, exclude_model=exclude_model,
                        exclude_kwargs=exclude_kwargs
                    )

                    try:
                        writer.delete_by_term('id', str(instance.pk))
                        writer.add_document(**kwargs)
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
            except whoosh.index.LockError:
                raise DynamicSearchRetry
            finally:
                lock.release()

    def index_search_model(self, search_model):
        self.clear_search_model_index(search_model=search_model)

        for instance in search_model.model._meta.managers_map[search_model.manager_name].all():
            self.index_instance(instance=instance)
