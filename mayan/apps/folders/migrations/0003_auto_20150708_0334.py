# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0002_auto_20150708_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='label',
            field=models.CharField(
                max_length=128, verbose_name='Label', db_index=True
            ),
            preserve_default=True,
        ),
    ]
