from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('file_metadata', '0003_auto_20191226_0606')
    ]

    operations = [
        migrations.RenameField(
            model_name='documentversiondriverentry',
            old_name='document_version',
            new_name='document_file',
        ),
    ]
