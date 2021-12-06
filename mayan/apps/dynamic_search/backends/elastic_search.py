from collections import deque
import logging

import elasticsearch
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Q, Search

from mayan.apps.common.utils import parse_range

from ..classes import SearchBackend, SearchModel
from ..settings import setting_results_limit

from .literals import DJANGO_TO_ELASTIC_SEARCH_FIELD_MAP

DEFAULT_ELASTIC_SEARCH_INDICES_NAMESPACE = 'mayan'
DEFAULT_ELASTIC_SEARCH_HOST = 'http://127.0.0.1:9200'
logger = logging.getLogger(name=__name__)


class ElasticSearchBackend(SearchBackend):
    _search_model_mappings = {}
    field_map = DJANGO_TO_ELASTIC_SEARCH_FIELD_MAP

    def __init__(self, **kwargs):
        self.indices_namespace = kwargs.pop(
            'indices_namespace', DEFAULT_ELASTIC_SEARCH_INDICES_NAMESPACE
        )
        self.host = kwargs.pop('host', DEFAULT_ELASTIC_SEARCH_HOST)
        self.hosts = kwargs.pop('hosts', None)

        super().__init__(**kwargs)

    def _search(
        self, query, search_model, user, global_and_search=False,
        ignore_limit=False
    ):
        client = self.get_client()
        index_name = self.get_index_name(
            search_model=search_model
        )

        search = Search(index=index_name, using=client)

        final_elastic_search_query = None

        for key, value in query.items():
            elastic_search_query = Q(
                Q(
                    name_or_query='fuzzy', _expand__to_dot=False, **{key: value}
                ) | Q(
                    name_or_query='match', _expand__to_dot=False, **{key: value}
                ) | Q(
                    name_or_query='regexp', _expand__to_dot=False, **{key: value}
                ) | Q(
                    name_or_query='wildcard', _expand__to_dot=False, **{key: value}
                )
            )

            if final_elastic_search_query is None:
                final_elastic_search_query = elastic_search_query
            else:
                if global_and_search:
                    final_elastic_search_query &= elastic_search_query
                else:
                    final_elastic_search_query |= elastic_search_query

        search = search.source(None).query(final_elastic_search_query)

        client.indices.refresh(index=index_name)

        if ignore_limit:
            limit = None
        else:
            limit = setting_results_limit.value

        response = search[0:limit].execute()

        id_list = []

        for hit in response:
            id_list.append(hit['id'])

        return search_model.get_queryset().filter(
            pk__in=id_list
        ).distinct()

    def deindex_instance(self, instance):
        search_model = SearchModel.get_for_model(instance=instance)
        client = self.get_client()
        client.delete(
            id=instance.pk,
            index=self.get_index_name(search_model=search_model)
        )

    def get_client(self):
        if not self.hosts:
            self.hosts = (self.host,)

        return Elasticsearch(
            hosts=self.hosts,
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60
        )

    def get_index_name(self, search_model):
        return '{}-{}'.format(
            self.indices_namespace, search_model.model_name.lower()
        )

    def get_status(self):
        client = self.get_client()
        result = []

        title = 'Elastic Search search model indexing status'
        result.append(title)
        result.append(len(title) * '=')

        stats = client.indices.stats()

        for search_model in SearchModel.all():
            index_name = self.get_index_name(search_model=search_model)
            index_stats = stats['indices'][index_name]

            result.append(
                '{}: {}'.format(
                    search_model.label, index_stats['total']['docs']['count']
                )
            )

        return result

    def index_instance(self, instance, exclude_model=None, exclude_kwargs=None):
        search_model = SearchModel.get_for_model(instance=instance)
        kwargs = search_model.populate(
            field_map=self.get_resolved_field_map(
                search_model=search_model
            ), instance=instance, exclude_model=exclude_model,
            exclude_kwargs=exclude_kwargs
        )

        self.get_client().index(
            index=self.get_index_name(search_model=search_model),
            id=instance.pk, document=kwargs
        )

    def index_search_model(self, search_model, range_string):
        client = self.get_client()
        index_name = self.get_index_name(search_model=search_model)
        field_map = self.get_resolved_field_map(
            search_model=search_model
        )

        def generate_actions():
            queryset = search_model.model._meta.managers_map[search_model.manager_name].all()

            for instance in queryset.filter(pk__in=parse_range(range_string=range_string)):
                kwargs = search_model.populate(
                    field_map=field_map, instance=instance
                )
                kwargs['id'] = instance.pk
                kwargs['_id'] = kwargs['id']
                yield kwargs

        bulk_indexing_generator = helpers.streaming_bulk(
            client=client, index=index_name, actions=generate_actions(),
            yield_ok=False
        )

        deque(iterable=bulk_indexing_generator, maxlen=0)

    def initialize(self):
        self.update_mappings()

    def reset(self):
        client = self.get_client()
        client.indices.delete(index='{}-*'.format(self.indices_namespace))
        self.update_mappings()

    def get_search_model_mappings(self, search_model):
        try:
            return self.__class__._search_model_mappings[search_model]
        except KeyError:
            mappings = {}

            field_map = self.get_resolved_field_map(search_model=search_model)
            for field_name, search_field_data in field_map.items():
                mappings[field_name] = {'type': search_field_data['field'].name}

            self.__class__._search_model_mappings[search_model] = mappings
            return mappings

    def update_mappings(self):
        client = self.get_client()

        actions = []
        for search_model in SearchModel.all():
            index_name = self.get_index_name(search_model=search_model)

            mappings = self.get_search_model_mappings(search_model=search_model)

            try:
                client.indices.create(
                    index=index_name,
                    body={'mappings': {'properties': mappings}}
                )
            except elasticsearch.exceptions.RequestError:
                try:
                    client.indices.put_mapping(
                        index=index_name,
                        body={'properties': mappings}
                    )
                except elasticsearch.exceptions.RequestError:
                    """There a mapping changes that were not allowed.
                    Example: Text to Keyword.
                    Boot up regardless and allow user to reindex to delete
                    old indices.
                    """
