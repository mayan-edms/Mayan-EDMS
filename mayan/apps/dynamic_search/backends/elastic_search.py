import logging

import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search

from ..classes import SearchBackend, SearchModel
from ..settings import setting_results_limit

from .literals import DJANGO_TO_ELASTIC_SEARCH_FIELD_MAP

DEFAULT_ELASTIC_SEARCH_INDICES_NAMESPACE = 'mayan'
DEFAULT_ELASTIC_SEARCH_HOST = 'http://127.0.0.1:9200'
logger = logging.getLogger(name=__name__)


class ElasticSearchBackend(SearchBackend):
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

        response = search.execute()

        id_list = []

        if ignore_limit:
            limit = None
        else:
            limit = setting_results_limit.value

        for hit in response[0:limit]:
            id_list.append(hit.meta.id)

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

    def index_instance(self, instance, exclude_model=None, exclude_kwargs=None):
        search_model = SearchModel.get_for_model(instance=instance)
        kwargs = search_model.populate(
            field_map=self.get_resolved_field_map(
                search_model=search_model
            ), instance=instance, exclude_model=exclude_model,
            exclude_kwargs=exclude_kwargs
        )

        kwargs['id'] = instance.id

        self.get_client().index(
            index=self.get_index_name(search_model=search_model),
            id=instance.pk, document=kwargs
        )

    def initialize(self):
        self.update_mappings()

    def reset(self):
        client = self.get_client()
        client.indices.delete(index='{}-*'.format(self.indices_namespace))
        self.update_mappings()

    def update_mappings(self):
        client = self.get_client()

        for search_model in SearchModel.all():
            index_name = self.get_index_name(search_model=search_model)

            body = {
                'mappings': {
                    'properties': {}
                }
            }

            field_map = self.get_resolved_field_map(search_model=search_model)
            for field_name, search_field_data in field_map.items():
                body['mappings']['properties'][field_name] = {'type': search_field_data['field'].name}

            try:
                client.indices.create(
                    index=index_name,
                    body=body
                )
            except elasticsearch.exceptions.RequestError:
                try:
                    client.indices.put_mapping(
                        index=index_name,
                        body=body['mappings']
                    )
                except elasticsearch.exceptions.RequestError:
                    """There a mapping changes that were not allowed.
                    Example: Text to Keyword.
                    Boot up regardless and allow user to reindex to delete
                    old indices.
                    """
