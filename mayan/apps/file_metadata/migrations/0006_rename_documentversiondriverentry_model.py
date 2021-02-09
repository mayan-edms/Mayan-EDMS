from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('file_metadata', '0005_rename_filemetadataentry_field'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentVersionDriverEntry',
            new_name='DocumentFileDriverEntry',
        )
    ]
