from django.apps import apps
from django.utils.encoding import force_text


def get_instance_ocr_content(instance):
    DocumentVersionPageOCRContent = apps.get_model(
        app_label='ocr', model_name='DocumentVersionPageOCRContent'
    )

    for page in instance.pages.all():
        try:
            page_content = page.ocr_content.content
        except DocumentVersionPageOCRContent.DoesNotExist:
            """Not critical, just ignore and go to next page."""
        else:
            yield force_text(s=page_content)
