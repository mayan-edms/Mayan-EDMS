import logging

from elasticsearch import Elasticsearch
from elasticsearch_dsl import AttrDict, Q, Search

from django.utils.encoding import force_text

from ..classes import SearchBackend, SearchField, SearchModel

from .literals import (
    QUERY_OPERATION_AND, QUERY_OPERATION_OR, TERM_NEGATION_CHARACTER,
    TERM_OPERATION_OR, TERM_OPERATIONS, TERM_QUOTES, TERM_SPACE_CHARACTER
)
logger = logging.getLogger(name=__name__)


class ElasticSearchBackend(SearchBackend):
    def _search(
        self, query, search_model, user, global_and_search=False,
        ignore_limit=False
    ):
        client = self.get_client()

        query_kwargs = {}

        search = Search(
            using=client, index=self.get_index_name(
                search_model=search_model
            )
        )

        elastic_search_query = Q('fuzzy', _expand__to_dot=False, **query) | Q('match', _expand__to_dot=False, **query) | Q('wildcard', _expand__to_dot=False, **query)
        search = search.query(elastic_search_query)

        client.indices.refresh(
            index=self.get_index_name(
                search_model=search_model
            )
        )

        response = search.execute()

        id_list = []

        for hit in response[0:100]:  #TODO change to setting
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
        #TODO: (host="localhost", port=9200
        return Elasticsearch(
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60
        )

    def get_index_name(self, search_model):
        return search_model.model_name.lower()

    def get_resolved_field_map(self, search_model):
        result = {}
        for search_field in self.get_search_model_fields(search_model=search_model):
            ##TODO:FIX
            from elasticsearch_dsl.field import Text
            backend_field_type = {'field': Text}


            if backend_field_type:
                result[search_field.get_full_name()] = backend_field_type
            else:
                logger.warning(
                    'Unknown field type "%s" for model "%s"',
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

    def index_instance(self, instance, exclude_model=None, exclude_kwargs=None):
        search_model = SearchModel.get_for_model(instance=instance)
        kwargs = search_model.populate(
            field_map=self.get_resolved_field_map(
                search_model=search_model
            ), instance=instance, exclude_model=exclude_model,
            exclude_kwargs=exclude_kwargs
        )

        kwargs['id'] = instance.id

        response = self.get_client().index(
            index=self.get_index_name(search_model=search_model),
            id=instance.pk, document=kwargs
        )
