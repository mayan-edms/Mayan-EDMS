# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_indexing', '0002_remove_index_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='index',
            old_name='title',
            new_name='label',
        ),
    ]
