from django.db import migrations


def operation_document_file_filename_copy(apps, schema_editor):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )
    document_iterator = Document.objects.using(alias=schema_editor.connection.alias).all().only('id', 'label').values_list('id', 'label').iterator()

    for document_id, label in document_iterator:
        DocumentFile.objects.filter(
            document_id=document_id
        ).update(filename=label)


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0066_documentfile_filename'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_document_file_filename_copy,
            reverse_code=migrations.RunPython.noop
        ),
    ]
