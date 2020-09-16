from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    document_file_page_search, document_search
)

__all__ = ()

document_file_page_search.add_model_field(
    field='document_file__document__workflows__log_entries__comment',
    label=_('Workflow transition comment')
)

document_search.add_model_field(
    field='workflows__log_entries__comment', label=_(
        'Workflow transition comment'
    )
)
