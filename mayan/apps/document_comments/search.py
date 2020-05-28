from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import document_page_search, document_search

document_page_search.add_model_field(
    field='document_version__document__comments__comment',
    label=_('Comments')
)
document_search.add_model_field(
    field='comments__comment',
    label=_('Comments')
)
