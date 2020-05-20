from django.db import migrations


def operation_create_file_metadata_setting_for_existing_document_types(apps, schema_editor):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    DocumentTypeSettings = apps.get_model(
        app_label='file_metadata', model_name='DocumentTypeSettings'
    )

    for document_type in DocumentType.objects.using(schema_editor.connection.alias).all():
        try:
            DocumentTypeSettings.objects.using(
                schema_editor.connection.alias
            ).get_or_create(document_type=document_type)
        except DocumentTypeSettings.DoesNotExist:
            pass


def operation_delete_file_metadata_setting_for_existing_document_types(apps, schema_editor):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    DocumentTypeSettings = apps.get_model(
        app_label='file_metadata', model_name='DocumentTypeSettings'
    )

    for document_type in DocumentType.objects.using(schema_editor.connection.alias).all():
        try:
            DocumentTypeSettings.objects.using(
                schema_editor.connection.alias
            ).get(document_type=document_type).delete()
        except DocumentTypeSettings.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0047_auto_20180917_0737'),
        ('file_metadata', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_create_file_metadata_setting_for_existing_document_types,
            reverse_code=operation_delete_file_metadata_setting_for_existing_document_types,
        )
    ]
