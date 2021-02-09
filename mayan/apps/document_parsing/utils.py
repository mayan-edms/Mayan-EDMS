from django.apps import apps
from django.utils.encoding import force_text
from django.utils.html import conditional_escape


def get_document_file_content(document_file):
    DocumentFilePageContent = apps.get_model(
        app_label='document_parsing', model_name='DocumentFilePageContent'
    )

    for page in document_file.pages.all():
        try:
            page_content = page.content.content
        except DocumentFilePageContent.DoesNotExist:
            pass
        else:
            yield conditional_escape(text=force_text(s=page_content))
