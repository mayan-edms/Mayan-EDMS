from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    document_version_search, document_version_page_search, document_search
)

# Document

document_search.add_model_field(
    field='versions__version_pages__ocr_content__content',
    label=_('Document version OCR')
)

# Document version

document_version_search.add_model_field(
    field='version_pages__ocr_content__content', label=_('OCR')
)

# Document version page

document_version_page_search.add_model_field(
    field='ocr_content__content', label=_('Document version OCR')
)
