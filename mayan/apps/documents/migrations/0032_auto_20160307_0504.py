# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import organizations.shortcuts


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0031_remove_document_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttype',
            name='organization',
            field=models.ForeignKey(default=organizations.shortcuts.get_current_organization, to='organizations.Organization'),
            preserve_default=True,
        ),
    ]
