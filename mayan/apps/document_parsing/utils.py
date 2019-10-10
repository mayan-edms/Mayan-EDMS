from __future__ import unicode_literals

from django.apps import apps
from django.utils.encoding import force_text
from django.utils.html import conditional_escape


def get_document_content(document):
    DocumentVersionPageContent = apps.get_model(
        app_label='document_parsing', model_name='DocumentVersionPageContent'
    )

    for document_page in document.pages.all():
        try:
            page_content = document_page.content_object.content.content
        except DocumentVersionPageContent.DoesNotExist:
            pass
        else:
            yield conditional_escape(force_text(page_content))


def get_document_version_content(document_version):
    DocumentVersionPageContent = apps.get_model(
        app_label='document_parsing', model_name='DocumentVersionPageContent'
    )

    for document_version_page in document_version.pages.all():
        try:
            page_content = document_version_page.content.content
        except DocumentVersionPageContent.DoesNotExist:
            pass
        else:
            yield conditional_escape(force_text(page_content))
