from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0010_rename_documentversionocrerror_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfileocrerror',
            options={'ordering': ('datetime_submitted',), 'verbose_name': 'Document file OCR error', 'verbose_name_plural': 'Document file OCR errors'},
        ),
        migrations.AlterField(
            model_name='documentfileocrerror',
            name='document_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_errors', to='documents.DocumentFile', verbose_name='Document file'),
        ),
    ]
