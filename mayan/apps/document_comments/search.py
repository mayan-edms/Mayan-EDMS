from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    search_model_document, search_model_document_file,
    search_model_document_file_page, search_model_document_version,
    search_model_document_version_page
)

# Document

search_model_document.add_model_field(
    field='comments__text', label=_('Comments')
)

# Document file

search_model_document_file.add_model_field(
    field='document__comments__text',
    label=_('Document comments')
)

# Document file page

search_model_document_file_page.add_model_field(
    field='document_file__document__comments__text',
    label=_('Document comments')
)

# Document version

search_model_document_version.add_model_field(
    field='document__comments__text',
    label=_('Document comments')
)

# Document version page

search_model_document_version_page.add_model_field(
    field='document_version__document__comments__text',
    label=_('Document comments')
)
