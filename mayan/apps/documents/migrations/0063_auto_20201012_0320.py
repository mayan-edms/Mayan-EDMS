from django.db import migrations, transaction


def pages_reset(
    document_id, DocumentFile, DocumentFilePage, DocumentVersion,
    DocumentVersionPage, content_type_id
):
    """
    Remove all page mappings and recreate them to be a 1 to 1 match
    to the latest document file or the document file supplied.
    """
    with transaction.atomic():
        document_version = DocumentVersion.objects.create(document_id=document_id)

        latest_file_id = DocumentFile.objects.filter(document_id=document_id).only('id').order_by('timestamp').last().id

        if latest_file_id:
            content_object_id_list = DocumentFilePage.objects.filter(
                document_file_id=latest_file_id
            ).only('id').values_list('id', flat=True).iterator()

            document_version_pages = [
                DocumentVersionPage(
                    document_version_id=document_version.id,
                    content_type_id=content_type_id,
                    object_id=content_object_id,
                    page_number=page_number
                ) for page_number, content_object_id in enumerate(
                    iterable=content_object_id_list, start=1
                )
            ]

            document_version.pages.bulk_create(document_version_pages)


def operation_document_version_page_create(apps, schema_editor):
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )
    DocumentFilePage = apps.get_model(
        app_label='documents', model_name='DocumentFilePage'
    )
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )
    DocumentVersionPage = apps.get_model(
        app_label='documents', model_name='DocumentVersionPage'
    )

    content_type = ContentType.objects.get(model='documentfilepage')

    document_id_iterator = Document.objects.using(alias=schema_editor.connection.alias).all().only('id').values_list('id', flat=True).iterator()

    for document_id in document_id_iterator:
        pages_reset(
            document_id=document_id,
            DocumentFile=DocumentFile,
            DocumentFilePage=DocumentFilePage,
            DocumentVersion=DocumentVersion,
            DocumentVersionPage=DocumentVersionPage,
            content_type_id=content_type.id,
        )


def operation_document_version_page_create_reverse(apps, schema_editor):
    DocumentVersionPage = apps.get_model(
        app_label='documents', model_name='DocumentVersionPage'
    )

    DocumentVersionPage.objects.using(schema_editor.connection.alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0062_auto_20200920_0614'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_document_version_page_create,
            reverse_code=operation_document_version_page_create_reverse
        ),
    ]
