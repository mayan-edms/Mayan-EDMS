from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    search_model_document, search_model_document_file,
    search_model_document_file_page, search_model_document_version,
    search_model_document_version_page
)

# Document

search_model_document.add_model_field(
    field='workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document file

search_model_document_file.add_model_field(
    field='document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document file page

search_model_document_file_page.add_model_field(
    field='document_file__document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document version

search_model_document_version.add_model_field(
    field='document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document version page

search_model_document_version_page.add_model_field(
    field='document_version__document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)
