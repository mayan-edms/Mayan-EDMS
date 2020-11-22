from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    document_file_search, document_file_page_search, document_search
)

# Document

document_search.add_model_field(
    field='files__file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
document_search.add_model_field(
    field='files__file_metadata_drivers__entries__value',
    label=_('File metadata value')
)

# Document file

document_file_search.add_model_field(
    field='file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
document_file_search.add_model_field(
    field='file_metadata_drivers__entries__value',
    label=_('File metadata value')
)

# Document file page

document_file_page_search.add_model_field(
    field='document_file__file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
document_file_page_search.add_model_field(
    field='document_file__file_metadata_drivers__entries__value',
    label=_('File metadata value')
)
