# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_add_data_default_organization'),
        ('acls', '0002_auto_20150703_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesscontrollist',
            name='organization',
            field=models.ForeignKey(default=organizations.shortcuts.get_current_organization, to='organizations.Organization'),
        ),
    ]
