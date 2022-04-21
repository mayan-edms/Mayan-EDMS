from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    search_model_document_file, search_model_document_file_page, search_model_document,
    search_model_document_version, search_model_document_version_page
)
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_metadata_type_view

# Document

search_model_document.add_model_field(
    field='metadata__metadata_type__name', label=_('Metadata type')
)
search_model_document.add_model_field(
    field='metadata__value', label=_('Metadata value')
)

# Document file

search_model_document_file.add_model_field(
    field='document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
search_model_document_file.add_model_field(
    field='document__metadata__value',
    label=_('Document metadata value')
)

# Document file page

search_model_document_file_page.add_model_field(
    field='document_file__document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
search_model_document_file_page.add_model_field(
    field='document_file__document__metadata__value',
    label=_('Document metadata value')
)

# Document version

search_model_document_version.add_model_field(
    field='document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
search_model_document_version.add_model_field(
    field='document__metadata__value',
    label=_('Document metadata value')
)

# Document version page

search_model_document_version_page.add_model_field(
    field='document_version__document__metadata__metadata_type__name',
    label=_('Document metadata type')
)
search_model_document_version_page.add_model_field(
    field='document_version__document__metadata__value',
    label=_('Document metadata value')
)

# Metadata type

search_model_metadata_type = SearchModel(
    app_label='metadata', model_name='MetadataType',
    permission=permission_metadata_type_view,
    serializer_path='mayan.apps.metadata.serializers.MetadataTypeSerializer'
)

search_model_metadata_type.add_model_field(field='default')
search_model_metadata_type.add_model_field(field='label')
search_model_metadata_type.add_model_field(field='lookup')
search_model_metadata_type.add_model_field(field='name')
search_model_metadata_type.add_model_field(field='parser')
search_model_metadata_type.add_model_field(field='validation')
