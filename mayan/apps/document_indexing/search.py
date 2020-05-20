from django.db import connection
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_document_indexing_instance_view


def transformation_format_uuid(term_string):
    if connection.vendor in ('mysql', 'sqlite'):
        return term_string.replace('-', '')
    else:
        return term_string


index_instance_node_search = SearchModel(
    app_label='document_indexing', model_name='IndexInstanceNodeSearchResult',
    permission=permission_document_indexing_instance_view,
    serializer_path='mayan.apps.document_indexing.serializers.IndexInstanceNodeSerializer'
)

index_instance_node_search.add_model_field(
    field='value', label=_('Value')
)

index_instance_node_search.add_model_field(
    field='documents__document_type__label', label=_('Document type')
)
index_instance_node_search.add_model_field(
    field='documents__versions__mimetype', label=_('Document MIME type')
)
index_instance_node_search.add_model_field(
    field='documents__label', label=_('Document label')
)
index_instance_node_search.add_model_field(
    field='documents__description', label=_('Document description')
)
index_instance_node_search.add_model_field(
    field='documents__uuid', label=_('Document UUID'),
    transformation_function=transformation_format_uuid
)
index_instance_node_search.add_model_field(
    field='documents__versions__checksum', label=_('Document checksum')
)
