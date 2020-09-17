from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('file_metadata', '0004_rename_documentversiondriverentry_field')
    ]

    operations = [
        migrations.RenameField(
            model_name='filemetadataentry',
            old_name='document_version_driver_entry',
            new_name='document_file_driver_entry',
        ),
    ]
