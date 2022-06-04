from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    search_model_document, search_model_document_file,
    search_model_document_file_page
)

# Document

search_model_document.add_model_field(
    field='files__file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
search_model_document.add_model_field(
    field='files__file_metadata_drivers__entries__value',
    label=_('File metadata value')
)

# Document file

search_model_document_file.add_model_field(
    field='file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
search_model_document_file.add_model_field(
    field='file_metadata_drivers__entries__value',
    label=_('File metadata value')
)

# Document file page

search_model_document_file_page.add_model_field(
    field='document_file__file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
search_model_document_file_page.add_model_field(
    field='document_file__file_metadata_drivers__entries__value',
    label=_('File metadata value')
)
