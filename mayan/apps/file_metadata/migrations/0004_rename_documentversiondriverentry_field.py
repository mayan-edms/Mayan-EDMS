from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0057_auto_20200916_1057'),
        ('file_metadata', '0003_auto_20191226_0606')
    ]

    operations = [
        migrations.RenameField(
            model_name='documentversiondriverentry',
            old_name='document_version',
            new_name='document_file',
        ),
    ]
