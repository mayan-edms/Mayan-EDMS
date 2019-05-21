from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models

import mayan.apps.document_signatures.models


class Migration(migrations.Migration):

    dependencies = [
        ('document_signatures', '0006_auto_20160326_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detachedsignature',
            name='signature_file',
            field=models.FileField(
                blank=True, null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location=b'mayan/media/document_storage'
                ), upload_to=mayan.apps.document_signatures.models.upload_to,
                verbose_name='Signature file'
            ),
        ),
    ]
