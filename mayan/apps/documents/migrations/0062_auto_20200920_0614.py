from django.db import migrations, models

import mayan.apps.documents.models.document_file_models
import mayan.apps.storage.classes


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0061_documentversionpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfilepage',
            name='enabled',
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='file',
            field=models.FileField(
                storage=mayan.apps.storage.classes.DefinedStorageLazy(
                    name='documents__documentfiles'
                ), upload_to=mayan.apps.documents.models.document_file_models.upload_to,
                verbose_name='File'
            ),
        ),
        migrations.AlterField(
            model_name='documentversionpage',
            name='page_number',
            field=models.PositiveIntegerField(
                db_index=True, default=1, editable=False,
                verbose_name='Page number'
            ),
        ),
    ]
