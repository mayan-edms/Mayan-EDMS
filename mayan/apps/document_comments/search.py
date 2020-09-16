from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    document_file_page_search, document_search
)

document_file_page_search.add_model_field(
    field='document_file__document__comments__comment',
    label=_('Comments')
)
document_search.add_model_field(
    field='comments__comment',
    label=_('Comments')
)
