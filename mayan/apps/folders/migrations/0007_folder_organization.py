# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('folders', '0006_auto_20160308_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='organization',
            field=models.ForeignKey(default=organizations.shortcuts.get_current_organization, to='organizations.Organization'),
        ),
    ]
