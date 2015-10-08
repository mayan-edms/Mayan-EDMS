# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0003_auto_20150708_0334'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFolder',
            fields=[
            ],
            options={
                'verbose_name': 'Document folder',
                'proxy': True,
                'verbose_name_plural': 'Document folders',
            },
            bases=('folders.folder',),
        ),
    ]
