from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.html import conditional_escape


def get_document_ocr_content(document):
    for page in document.pages.all():
        try:
            page_content = page.ocr_content.content
        except DocumentPageContent.DoesNotExist:
            pass
        else:
            yield conditional_escape(force_text(page_content))
