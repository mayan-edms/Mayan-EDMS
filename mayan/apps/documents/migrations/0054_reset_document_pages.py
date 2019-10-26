from __future__ import unicode_literals

from django.db import migrations


def get_latest_version(document):
    return document.versions.order_by('timestamp').last()


def operation_reset_document_pages(apps, schema_editor):
    Document = apps.get_model(app_label='documents', model_name='Document')

    # Define inside the function to use the migration's apps instance
    def pages_reset(document):
        ContentType = apps.get_model('contenttypes', 'ContentType')
        DocumentVersionPage = apps.get_model(
            app_label='documents', model_name='DocumentVersionPage'
        )

        content_type = ContentType.objects.get_for_model(
            model=DocumentVersionPage
        )

        for document_page in document.pages.all():
            document_page.delete()

        latest_version = get_latest_version(document=document)
        if latest_version:
            for version_page in latest_version.pages.all():
                document_page = document.pages.create(
                    content_type=content_type,
                    page_number=version_page.page_number,
                    object_id=version_page.pk,
                )

    for document in Document.objects.using(schema_editor.connection.alias).all():
        pages_reset(document=document)


def operation_reset_document_pages_reverse(apps, schema_editor):
    Document = apps.get_model(app_label='documents', model_name='Document')

    for document in Document.objects.using(schema_editor.connection.alias).all():
        for document_page in document.pages.all():
            document_page.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0053_create_document_page_and_result_models'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_reset_document_pages,
            reverse_code=operation_reset_document_pages_reverse
        ),
    ]
