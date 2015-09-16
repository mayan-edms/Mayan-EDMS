# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={
                'ordering': ('label',), 'verbose_name': 'Folder',
                'verbose_name_plural': 'Folders'
            },
        ),
        migrations.RenameField(
            model_name='folder',
            old_name='title',
            new_name='label',
        ),
        migrations.AlterUniqueTogether(
            name='folder',
            unique_together=set([('label', 'user')]),
        ),
    ]
