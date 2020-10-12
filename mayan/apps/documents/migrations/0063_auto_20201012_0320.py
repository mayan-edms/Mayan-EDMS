from django.db import migrations


def pages_reset(content_type, document_version):
    """
    Remove all page mappings and recreate them to be a 1 to 1 match
    to the latest document file or the document file supplied.
    """
    latest_file = document_version.document.files.order_by('timestamp').last()

    if latest_file:
        content_object_list = list(latest_file.file_pages.all())
    else:
        content_object_list = ()

    for page_number, content_object in enumerate(iterable=content_object_list, start=1):
        document_version.pages.create(
            content_type=content_type,
            object_id=content_object.pk,
            page_number=page_number
        )


def operation_document_version_page_create(apps, schema_editor):
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )

    content_type = ContentType.objects.get(model='documentfilepage')

    for document in Document.objects.using(schema_editor.connection.alias).all():
        document_version = document.versions.create()
        pages_reset(content_type=content_type, document_version=document_version)


def operation_document_version_page_create_reverse(apps, schema_editor):
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    for document_version in DocumentVersion.objects.using(schema_editor.connection.alias).all():
        document_version.delete()


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
