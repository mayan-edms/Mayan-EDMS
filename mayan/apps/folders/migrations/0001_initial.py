# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'title', models.CharField(
                        max_length=128, verbose_name='Title', db_index=True
                    )
                ),
                (
                    'datetime_created', models.DateTimeField(
                        auto_now_add=True, verbose_name='Datetime created'
                    )
                ),
                (
                    'documents', models.ManyToManyField(
                        related_name='folders', verbose_name='Documents',
                        to='documents.Document'
                    )
                ),
                (
                    'user', models.ForeignKey(
                        verbose_name='User', to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Folder',
                'verbose_name_plural': 'Folders',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='folder',
            unique_together=set([('title', 'user')]),
        ),
    ]
