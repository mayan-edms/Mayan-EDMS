# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_auto_20150628_0533'),
        ('acls', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CreatorSingleton',
        ),
        migrations.RemoveField(
            model_name='defaultaccessentry',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='defaultaccessentry',
            name='holder_type',
        ),
        migrations.RemoveField(
            model_name='defaultaccessentry',
            name='permission',
        ),
        migrations.DeleteModel(
            name='DefaultAccessEntry',
        ),
        migrations.RemoveField(
            model_name='accessentry',
            name='holder_id',
        ),
        migrations.RemoveField(
            model_name='accessentry',
            name='holder_type',
        ),
        migrations.AddField(
            model_name='accessentry',
            name='role',
            field=models.ForeignKey(default=1, verbose_name='Role', to='permissions.Role'),
            preserve_default=False,
        ),
    ]
