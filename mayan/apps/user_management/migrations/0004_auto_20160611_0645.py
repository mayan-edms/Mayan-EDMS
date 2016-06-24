# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import organizations.shortcuts
import user_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_auto_20160525_0155'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='mayanuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
                ('on_organization', user_management.models.OrganizationUserManagerHybridClass()),
            ],
        ),
        migrations.AlterField(
            model_name='mayanuser',
            name='organization',
            field=models.ForeignKey(default=organizations.shortcuts.get_current_organization, blank=True, to='organizations.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='mayanuser',
            name='organization_groups',
            field=models.ManyToManyField(related_query_name='user', related_name='users', to='user_management.MayanGroup', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='Groups'),
        ),
    ]
