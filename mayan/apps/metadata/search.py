from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    document_file_search, document_file_page_search, document_search,
    document_version_search, document_version_page_search
)
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_metadata_type_view

# Document

document_search.add_model_field(
    field='metadata__metadata_type__name', label=_('Metadata type')
)
document_search.add_model_field(
    field='metadata__value', label=_('Metadata value')
)

# Document file

document_file_search.add_model_field(
    field='document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
document_file_search.add_model_field(
    field='document__metadata__value',
    label=_('Document metadata value')
)

# Document file page

document_file_page_search.add_model_field(
    field='document_file__document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
document_file_page_search.add_model_field(
    field='document_file__document__metadata__value',
    label=_('Document metadata value')
)

# Document version

document_version_search.add_model_field(
    field='document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
document_version_search.add_model_field(
    field='document__metadata__value',
    label=_('Document metadata value')
)

# Document version page

document_version_page_search.add_model_field(
    field='document_version__document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
document_version_page_search.add_model_field(
    field='document_version__document__metadata__value',
    label=_('Document metadata value')
)

# Metadata type

metadata_type_search = SearchModel(
    app_label='metadata', model_name='MetadataType',
    permission=permission_metadata_type_view,
    serializer_path='mayan.apps.metadata.serializers.MetadataTypeSerializer'
)

metadata_type_search.add_model_field(field='default')
metadata_type_search.add_model_field(field='label')
metadata_type_search.add_model_field(field='lookup')
metadata_type_search.add_model_field(field='name')
metadata_type_search.add_model_field(field='parser')
metadata_type_search.add_model_field(field='validation')
