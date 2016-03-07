# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50, verbose_name='Label')),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
            bases=(models.Model,),
        ),
    ]
