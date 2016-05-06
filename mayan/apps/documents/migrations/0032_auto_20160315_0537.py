# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import connection, migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0031_convert_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]

    def __init__(self, *args, **kwargs):
        super(Migration, self).__init__(*args, **kwargs)

        if connection.vendor == 'postgresql':
            self.operations.insert(
                0, migrations.RunSQL(
                    'ALTER TABLE documents_document ALTER COLUMN uuid SET DATA TYPE UUID USING uuid::uuid;'
                )
            )
