import mayan.apps.common.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0009_auto_20180402_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareduploadedfile',
            name='file',
            field=models.FileField(
                storage=django.core.files.storage.FileSystemStorage(
                    location=b'mayan/media/shared_files'
                ), upload_to=mayan.apps.common.models.upload_to,
                verbose_name='File'
            ),
        ),
    ]
