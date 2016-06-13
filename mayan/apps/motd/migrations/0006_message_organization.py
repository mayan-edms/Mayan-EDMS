# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_add_data_default_organization'),
        ('motd', '0005_auto_20160510_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='organization',
            field=models.ForeignKey(
                default=organizations.shortcuts.get_current_organization,
                to='organizations.Organization'
            ),
        ),
    ]
