from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0010_auto_20201012_0914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentversionocrerror',
            options={'ordering': ('datetime_submitted',), 'verbose_name': 'Document version OCR error', 'verbose_name_plural': 'Document version OCR errors'},
        ),
        migrations.AlterModelOptions(
            name='documentversionpageocrcontent',
            options={'verbose_name': 'Document version page OCR content', 'verbose_name_plural': 'Document version pages OCR contents'},
        ),
        migrations.AlterField(
            model_name='documentversionocrerror',
            name='document_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_errors', to='documents.DocumentVersion', verbose_name='Document version'),
        ),
        migrations.AlterField(
            model_name='documentversionpageocrcontent',
            name='document_version_page',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_content', to='documents.DocumentVersionPage', verbose_name='Document version page'),
        ),
    ]
