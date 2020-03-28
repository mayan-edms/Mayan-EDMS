import uuid

from django.db import models, migrations
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import force_text


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0002_auto_20150608_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uuid',
            field=models.CharField(
                default=force_text(uuid.uuid4()), max_length=48,
                editable=False
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentversion',
            name='file',
            field=models.FileField(
                upload_to=force_text(uuid.uuid4()),
                storage=FileSystemStorage(),
                verbose_name='File'
            ),
            preserve_default=True,
        ),
    ]
