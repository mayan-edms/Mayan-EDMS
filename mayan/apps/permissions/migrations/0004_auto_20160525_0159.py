# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_add_data_default_organization'),
        ('user_management', '0003_auto_20160525_0155'),
        ('permissions', '0003_remove_role_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='groups',
        ),
        migrations.AddField(
            model_name='role',
            name='organization',
            field=models.ForeignKey(default=organizations.shortcuts.get_current_organization, to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='role',
            name='organization_groups',
            field=models.ManyToManyField(related_name='roles', verbose_name='Groups', to='user_management.MayanGroup'),
        ),
    ]
