# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_add_data_default_organization'),
        ('linking', '0005_auto_20150729_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartlink',
            name='organization',
            field=models.ForeignKey(
                default=organizations.shortcuts.get_current_organization,
                to='organizations.Organization'
            ),
        ),
    ]
