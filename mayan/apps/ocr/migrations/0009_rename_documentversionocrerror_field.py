from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0008_auto_20180917_0646')
    ]

    operations = [
        migrations.RenameField(
            model_name='documentversionocrerror',
            old_name='document_version',
            new_name='document_file',
        ),
    ]
