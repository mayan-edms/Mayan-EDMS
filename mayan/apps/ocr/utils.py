from __future__ import unicode_literals

from django.apps import apps
from django.utils.encoding import force_text


def get_instance_ocr_content(instance):
    DocumentPageOCRContent = apps.get_model(
        app_label='ocr', model_name='DocumentPageOCRContent'
    )

    for page in instance.pages.all():
        try:
            page_content = page.ocr_content.content
        except DocumentPageOCRContent.DoesNotExist:
            pass
        else:
            yield force_text(page_content)
