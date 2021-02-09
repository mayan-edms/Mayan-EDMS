from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    document_file_search, document_file_page_search, document_search,
    document_version_search, document_version_page_search
)

# Document

document_search.add_model_field(
    field='workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document file

document_file_search.add_model_field(
    field='document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document file page

document_file_page_search.add_model_field(
    field='document_file__document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document version

document_version_search.add_model_field(
    field='document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)

# Document version page

document_version_page_search.add_model_field(
    field='document_version__document__workflows__log_entries__comment',
    label=_('Document workflow transition comment')
)
