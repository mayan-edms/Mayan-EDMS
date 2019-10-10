from __future__ import unicode_literals

from django.apps import apps
from django.utils.encoding import force_text


def get_document_version_ocr_content(document_version):
    DocumentVersionPageOCRContent = apps.get_model(
        app_label='ocr', model_name='DocumentVersionPageOCRContent'
    )

    for document_version_page in document_version.pages.all():
        try:
            page_content = document_version_page.ocr_content.content
        except DocumentVersionPageOCRContent.DoesNotExist:
            pass
        else:
            yield force_text(page_content)


def get_document_ocr_content(document):
    DocumentVersionPageOCRContent = apps.get_model(
        app_label='ocr', model_name='DocumentVersionPageOCRContent'
    )

    for document_page in document.pages.all():
        try:
            page_content = document_page.content_object.ocr_content.content
        except (AttributeError, DocumentVersionPageOCRContent.DoesNotExist):
            pass
        else:
            yield force_text(page_content)
