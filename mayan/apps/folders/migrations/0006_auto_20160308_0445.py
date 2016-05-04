# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0005_auto_20160308_0437'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='folder',
            unique_together=set([('label',)]),
        ),
        migrations.RemoveField(
            model_name='folder',
            name='user',
        ),
    ]
