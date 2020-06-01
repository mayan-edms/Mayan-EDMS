from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('storage', '0002_auto_20200528_0826'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StorageSharedUploadedFile',
            new_name='SharedUploadedFile',
        ),
    ]
