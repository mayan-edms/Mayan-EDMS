# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_add_data_default_organization'),
        ('django_gpg', '0006_auto_20160510_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='organization',
            field=models.ForeignKey(default=organizations.shortcuts.get_current_organization, to='organizations.Organization'),
        ),
    ]
