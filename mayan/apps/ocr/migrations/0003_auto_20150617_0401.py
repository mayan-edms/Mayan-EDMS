from django.db import migrations


def operation_move_content_from_documents_to_ocr_app(apps, schema_editor):
    DocumentPage = apps.get_model(
        app_label='documents', model_name='DocumentPage'
    )
    DocumentPageContent = apps.get_model(
        app_label='ocr', model_name='DocumentPageContent'
    )

    for document_page in DocumentPage.objects.using(schema_editor.connection.alias).all():
        DocumentPageContent.objects.using(schema_editor.connection.alias).create(
            document_page=document_page,
            content=document_page.content_old or ''
        )


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0002_documentpagecontent'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_move_content_from_documents_to_ocr_app
        ),
    ]
