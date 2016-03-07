# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('documents', '0028_newversionblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttype',
            name='organization',
            field=models.ForeignKey(default=1, to='organizations.Organization'),
            preserve_default=False,
        ),
    ]
