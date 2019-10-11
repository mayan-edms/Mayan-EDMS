from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0008_auto_20180917_0646'),
        ('documents', '0052_rename_document_page'),
    ]

    operations = [
        migrations.RenameModel(
            'DocumentPageOCRContent', 'DocumentVersionPageOCRContent'
        ),
        migrations.AlterField(
            model_name='documentversionpageocrcontent',
            name='document_page',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_content',
                to='documents.DocumentVersionPage',
                verbose_name='Document version page'
            ),
        ),
        migrations.RenameField(
            model_name='documentversionpageocrcontent',
            old_name='document_page',
            new_name='document_version_page',
        ),
        migrations.AlterModelOptions(
            name='documentversionpageocrcontent',
            options={
                'verbose_name': 'Document version page OCR content',
                'verbose_name_plural': 'Document version pages OCR contents'
            },
        ),
    ]
