from django.db import migrations, models

import mayan.apps.storage.classes
import mayan.apps.storage.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StorageSharedUploadedFile',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'file', models.FileField(
                        storage=mayan.apps.storage.classes.DefinedStorageLazy(
                            name='storage__shareduploadedfile'
                        ), upload_to=mayan.apps.storage.models.upload_to,
                        verbose_name='File'
                    )
                ),
                (
                    'filename', models.CharField(
                        max_length=255, verbose_name='Filename'
                    )
                ),
                (
                    'datetime', models.DateTimeField(
                        auto_now_add=True, verbose_name='Date time'
                    )
                ),
            ],
            options={
                'verbose_name': 'Shared uploaded file',
                'verbose_name_plural': 'Shared uploaded files',
            },
        ),
    ]
