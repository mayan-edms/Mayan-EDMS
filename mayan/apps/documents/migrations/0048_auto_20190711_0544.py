import uuid

from django.db import migrations, models
from django.utils.encoding import force_text

import mayan.apps.storage.classes


def UUID_FUNCTION(*args, **kwargs):
    return force_text(s=uuid.uuid4())


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
                upload_to=UUID_FUNCTION,
                verbose_name='File'
            ),
        ),
    ]
