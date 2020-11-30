from django.db import migrations


def operation_duplicated_document_old_copy(apps, schema_editor):
    DuplicatedDocumentOld = apps.get_model(
        app_label='documents', model_name='DuplicatedDocumentOld'
    )
    DuplicatedDocument = apps.get_model(
        app_label='duplicates', model_name='DuplicatedDocument'
    )

    model_iterator = DuplicatedDocumentOld.objects.using(
        alias=schema_editor.connection.alias
    ).all().only('document_id', 'datetime_added').iterator()

    for model_instance in model_iterator:
        new_instance = DuplicatedDocument.objects.create(
            document_id=model_instance.document_id,
            datetime_added=model_instance.datetime_added
        )
        new_instance.documents.add(
            *model_instance.documents.only('pk').values_list('id', flat=True)
        )


def operation_duplicated_document_old_copy_reverse(apps, schema_editor):
    DuplicatedDocumentOld = apps.get_model(
        app_label='documents', model_name='DuplicatedDocumentOld'
    )
    DuplicatedDocument = apps.get_model(
        app_label='duplicates', model_name='DuplicatedDocument'
    )

    model_iterator = DuplicatedDocument.objects.using(
        alias=schema_editor.connection.alias
    ).all().only('document_id', 'datetime_added').iterator()

    for model_instance in model_iterator:
        new_instance = DuplicatedDocumentOld.objects.create(
            document_id=model_instance.document_id,
            datetime_added=model_instance.datetime_added
        )
        new_instance.documents.add(
            *model_instance.documents.only('pk').values_list('id', flat=True)
        )


class Migration(migrations.Migration):
    dependencies = [
        ('duplicates', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_duplicated_document_old_copy,
            reverse_code=operation_duplicated_document_old_copy_reverse
        ),
    ]

    run_before = [
        ('documents', '0075_delete_duplicateddocumentold'),
    ]
