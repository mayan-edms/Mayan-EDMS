# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def merge_label_and_user(apps, schema_editor):
    Folder = apps.get_model('folders', 'Folder')

    for folder in Folder.objects.all():
        folder.label = '{}-{}'.format(folder.user.username, folder.label)
        folder.save()


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0004_documentfolder'),
    ]

    operations = [
        migrations.RunPython(merge_label_and_user),
    ]
