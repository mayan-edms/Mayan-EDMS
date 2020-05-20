import django.core.files.storage
from django.db import migrations, models

import mayan.apps.document_signatures.models


class Migration(migrations.Migration):
    dependencies = [
        ('document_signatures', '0007_auto_20180403_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detachedsignature',
            name='signature_file',
            field=models.FileField(
                blank=True, null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location=b'/home/rosarior/development/mayan-edms/mayan/media/document_signatures'
                ),
                upload_to=mayan.apps.document_signatures.models.upload_to,
                verbose_name='Signature file'
            ),
        ),
    ]
