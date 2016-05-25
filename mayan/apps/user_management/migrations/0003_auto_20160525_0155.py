# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_add_data_default_organization'),
        ('auth', '0006_require_contenttypes_0002'),
        ('user_management', '0002_auto_20160504_0638'),
    ]

    operations = [
        migrations.CreateModel(
            name='MayanGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('organization', models.ForeignKey(default=organizations.shortcuts.get_current_organization, to='organizations.Organization')),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='mayanuser',
            name='organization_groups',
            field=models.ManyToManyField(related_query_name='user', related_name='organization_user_set', to='user_management.MayanGroup', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='Groups'),
        ),
    ]
