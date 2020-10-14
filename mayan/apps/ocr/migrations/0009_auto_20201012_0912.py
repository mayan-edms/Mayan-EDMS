from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0064_auto_20201012_0544'),
        ('ocr', '0008_auto_20180917_0646'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentPageOCRContent',
            new_name='DocumentVersionPageOCRContent',
        ),
        migrations.AlterModelOptions(
            name='documentversionocrerror',
            options={
                'ordering': ('datetime_submitted',),
                'verbose_name': 'Document file OCR error',
                'verbose_name_plural': 'Document file OCR errors'
            },
        ),
        migrations.AlterField(
            model_name='documentversionocrerror',
            name='document_version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_errors', to='documents.DocumentVersion',
                verbose_name='Document file'
            ),
        ),
        migrations.AlterField(
            model_name='documentversionpageocrcontent',
            name='document_page',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_content',
                to='documents.DocumentVersionPage',
                verbose_name='Document page'
            ),
        ),
    ]
