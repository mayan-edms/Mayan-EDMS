from __future__ import unicode_literals

from django.db import migrations, models
import mayan.apps.documents.models.document_version_models
import mayan.apps.storage.classes


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0047_auto_20180917_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentversion',
            name='file',
            field=models.FileField(
                storage=mayan.apps.storage.classes.FakeStorageSubclass(),
                upload_to=mayan.apps.documents.models.document_version_models.UUID_FUNCTION,
                verbose_name='File'
            ),
        ),
    ]
