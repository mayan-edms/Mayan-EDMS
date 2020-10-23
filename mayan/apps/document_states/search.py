from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import document_search, document_page_search

__all__ = ()

document_search.add_model_field(
    field='workflows__log_entries__comment', label=_(
        'Workflow transition comment'
    )
)
document_page_search.add_model_field(
    field='document_version__document__workflows__log_entries__comment',
    label=_('Workflow transition comment')
)
