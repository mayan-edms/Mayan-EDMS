# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0030_document_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='organization',
        ),
    ]
