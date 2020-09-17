from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0009_rename_documentversionocrerror_field'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentVersionOCRError',
            new_name='DocumentFileOCRError',
        )
    ]
