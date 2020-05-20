from django.db import migrations, models

import mayan.apps.document_signatures.models
import mayan.apps.storage.classes


class Migration(migrations.Migration):
    dependencies = [
        ('document_signatures', '0008_auto_20180429_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detachedsignature',
            name='signature_file',
            field=models.FileField(
                blank=True, null=True,
                storage=mayan.apps.storage.classes.FakeStorageSubclass(),
                upload_to=mayan.apps.document_signatures.models.upload_to,
                verbose_name='Signature file'
            ),
        ),
    ]
