from django.db import migrations, models
import django.db.models.deletion


def code_delete_document_version_page_ocr_errors(apps, schema_editor):
    DocumentVersionOCRError = apps.get_model(
        app_label='ocr', model_name='DocumentVersionOCRError'
    )
    DocumentVersionOCRError.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0075_delete_duplicateddocumentold'),
        ('ocr', '0009_auto_20210304_0950'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentTypeSettings',
            new_name='DocumentTypeOCRSettings',
        ),
        migrations.RunPython(
            code=code_delete_document_version_page_ocr_errors,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='documentversionocrerror',
            name='document_version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_errors', to='documents.DocumentVersion',
                verbose_name='Document version'
            ),
        ),
        migrations.DeleteModel(
            name='DocumentPageOCRContent',
        ),
    ]
