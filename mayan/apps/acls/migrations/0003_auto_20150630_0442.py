# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('permissions', '0002_auto_20150628_0533'),
        ('acls', '0002_auto_20150629_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessControlList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name='object_content_type', to='contenttypes.ContentType')),
                ('permissions', models.ManyToManyField(related_name='acls', verbose_name='Permissions', to='permissions.StoredPermission')),
                ('role', models.ForeignKey(related_name='acls', verbose_name='Role', to='permissions.Role')),
            ],
            options={
                'verbose_name': 'Access entry',
                'verbose_name_plural': 'Access entries',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='accessentry',
            name='content_type',
            field=models.ForeignKey(related_name='object_content_type_1', to='contenttypes.ContentType'),
            preserve_default=True,
        ),
    ]
