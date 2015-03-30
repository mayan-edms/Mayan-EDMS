# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storage.backends.filebasedstorage


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uuid',
            field=models.CharField(default='86da1aac-f75b-418b-987c-cfcdd370355b', max_length=48, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentversion',
            name='file',
            field=models.FileField(upload_to='7e2f3d5f-f691-418a-a30c-f291f7ab9904', storage=storage.backends.filebasedstorage.FileBasedStorage(), verbose_name='File'),
            preserve_default=True,
        ),
    ]
