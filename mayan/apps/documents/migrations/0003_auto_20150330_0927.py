# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storage.backends.filebasedstorage


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20150330_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uuid',
            field=models.CharField(default='cc4f2ad1-a27b-4e7e-8942-adafadb345f8', max_length=48, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentversion',
            name='file',
            field=models.FileField(upload_to='704291c2-4b80-46c9-96fc-8b17825232f1', storage=storage.backends.filebasedstorage.FileBasedStorage(), verbose_name='File'),
            preserve_default=True,
        ),
    ]
