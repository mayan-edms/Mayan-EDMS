from collections import deque
import logging

import elasticsearch
from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Q, Search

from mayan.apps.common.utils import parse_range

from ..classes import SearchBackend, SearchModel
from ..exceptions import DynamicSearchException
from ..settings import setting_results_limit

from .literals import (
    DEFAULT_ELASTICSEARCH_CLIENT_MAXSIZE,
    DEFAULT_ELASTICSEARCH_CLIENT_SNIFF_ON_START,
    DEFAULT_ELASTICSEARCH_CLIENT_SNIFF_ON_CONNECTION_FAIL,
    DEFAULT_ELASTICSEARCH_CLIENT_SNIFFER_TIMEOUT, DEFAULT_ELASTICSEARCH_HOST,
    DEFAULT_ELASTICSEARCH_INDICES_NAMESPACE,
    DJANGO_TO_ELASTICSEARCH_FIELD_MAP
)

logger = logging.getLogger(name=__name__)


class ElasticSearchBackend(SearchBackend):
    _client = None
    _search_model_mappings = {}
    field_map = DJANGO_TO_ELASTICSEARCH_FIELD_MAP

    def __init__(self, **kwargs):
        self.client_kwargs = {}

        self.indices_namespace = kwargs.pop(
            'indices_namespace', DEFAULT_ELASTICSEARCH_INDICES_NAMESPACE
        )

        host = kwargs.pop('client_host', DEFAULT_ELASTICSEARCH_HOST)
        hosts = kwargs.pop('client_hosts', None)

        if not hosts:
            hosts = (host,)

        self.client_kwargs['hosts'] = hosts

        self.client_kwargs['http_auth'] = kwargs.pop('client_http_auth', None)
        self.client_kwargs['port'] = kwargs.pop('client_port', None)
        self.client_kwargs['scheme'] = kwargs.pop('client_scheme', None)

        self.client_kwargs['maxsize'] = kwargs.pop(
            'client_maxsize', DEFAULT_ELASTICSEARCH_CLIENT_MAXSIZE
        )
        self.client_kwargs['sniff_on_start'] = kwargs.pop(
            'client_sniff_on_start', DEFAULT_ELASTICSEARCH_CLIENT_SNIFF_ON_START
        )
        self.client_kwargs['sniff_on_connection_fail'] = kwargs.pop(
            'client_sniff_on_connection_fail', DEFAULT_ELASTICSEARCH_CLIENT_SNIFF_ON_CONNECTION_FAIL
        )
        self.client_kwargs['sniffer_timeout'] = kwargs.pop(
            'client_sniffer_timeout', DEFAULT_ELASTICSEARCH_CLIENT_SNIFFER_TIMEOUT
        )

        super().__init__(**kwargs)

    def _get_status(self):
        client = self.get_client()
        result = []

        title = 'Elastic Search search model indexing status'
        result.append(title)
        result.append(len(title) * '=')

        stats = client.indices.stats()

        for search_model in SearchModel.all():
            index_name = self.get_index_name(search_model=search_model)
            index_stats = stats['indices'].get(index_name, {})
            if index_stats:
                count = index_stats['total']['docs']['count']
            else:
                count = '-1'

            result.append(
                '{}: {}'.format(search_model.label, count)
            )

        return '\n'.join(result)

    def _initialize(self):
        self.update_mappings()

    def _search(
        self, query, search_model, user, global_and_search=False,
        ignore_limit=False
    ):
        client = self.get_client()
        index_name = self.get_index_name(
            search_model=search_model
        )

        search = Search(index=index_name, using=client)

        final_elasticsearch_query = None

        for key, value in query.items():
            elasticsearch_query = Q(
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

            if final_elasticsearch_query is None:
                final_elasticsearch_query = elasticsearch_query
            else:
                if global_and_search:
                    final_elasticsearch_query &= elasticsearch_query
                else:
                    final_elasticsearch_query |= elasticsearch_query

        search = search.source(None).query(final_elasticsearch_query)

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

    def close(self):
        self.get_client().transport.close()
        self.__class__._client = None

    def deindex_instance(self, instance):
        search_model = SearchModel.get_for_model(instance=instance)
        client = self.get_client()
        client.delete(
            id=instance.pk,
            index=self.get_index_name(search_model=search_model)
        )

    def get_client(self):
        try:
            if self.__class__._client is None:
                self.__class__._client = Elasticsearch(**self.client_kwargs)
        except Exception as exception:
            raise DynamicSearchException(
                'Unable to instantiate client; {}'.format(self.client_kwargs)
            ) from exception

        return self.__class__._client

    def get_index_name(self, search_model):
        return '{}-{}'.format(
            self.indices_namespace, search_model.model_name.lower()
        )

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

    def index_instance(self, instance, exclude_model=None, exclude_kwargs=None):
        search_model = SearchModel.get_for_model(instance=instance)

        document = search_model.populate(
            backend=self, instance=instance, exclude_model=exclude_model,
            exclude_kwargs=exclude_kwargs
        )

        self.get_client().index(
            index=self.get_index_name(search_model=search_model),
            id=instance.pk, document=document
        )

    def index_search_model(self, search_model, range_string=None):
        client = self.get_client()
        index_name = self.get_index_name(search_model=search_model)

        def generate_actions():
            queryset = search_model.get_queryset()

            if range_string:
                queryset = queryset.filter(pk__in=list(parse_range(range_string=range_string)))

            for instance in queryset:
                kwargs = search_model.populate(
                    backend=self, instance=instance
                )
                kwargs['_id'] = kwargs['id']

                yield kwargs

        bulk_indexing_generator = helpers.streaming_bulk(
            client=client, index=index_name, actions=generate_actions(),
            yield_ok=False
        )

        deque(iterable=bulk_indexing_generator, maxlen=0)

    def reset(self, search_model=None):
        self.tear_down(search_model=search_model)
        self.update_mappings(search_model=search_model)

    def tear_down(self, search_model=None):
        client = self.get_client()
        if search_model:
            client.indices.delete(
                index=self.get_index_name(search_model=search_model)
            )
        else:
            client.indices.delete(
                index='{}-*'.format(self.indices_namespace)
            )

    def update_mappings(self, search_model=None):
        client = self.get_client()

        if search_model:
            search_models = (search_model,)
        else:
            search_models = SearchModel.all()

        for search_model in search_models:
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
