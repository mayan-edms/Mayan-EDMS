from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import document_page_search, document_search

document_search.add_model_field(
    field='versions__file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
document_search.add_model_field(
    field='versions__file_metadata_drivers__entries__value',
    label=_('File metadata value')
)

document_page_search.add_model_field(
    field='document_version__file_metadata_drivers__entries__key',
    label=_('File metadata key')
)
document_page_search.add_model_field(
    field='document_version__file_metadata_drivers__entries__value',
    label=_('File metadata value')
)
