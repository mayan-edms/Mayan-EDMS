from django.db import models, migrations


def operation_create_ocr_setting_for_existing_document_types(apps, schema_editor):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    DocumentTypeSettings = apps.get_model(
        app_label='ocr', model_name='DocumentTypeSettings'
    )

    for document_type in DocumentType.objects.using(schema_editor.connection.alias).all():
        try:
            DocumentTypeSettings.objects.using(
                schema_editor.connection.alias
            ).create(document_type=document_type)
        except DocumentTypeSettings.DoesNotExist:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0016_auto_20150708_0325'),
        ('ocr', '0003_auto_20150617_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTypeSettings',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'auto_ocr', models.BooleanField(
                        default=True,
                        verbose_name='Automatically queue newly created '
                        'documents for OCR.'
                    )
                ),
                (
                    'document_type', models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name='ocr_settings',
                        to='documents.DocumentType',
                        verbose_name='Document type'
                    )
                ),
            ],
            options={
                'verbose_name': 'Document type settings',
                'verbose_name_plural': 'Document types settings',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(
            code=operation_create_ocr_setting_for_existing_document_types
        ),
    ]
