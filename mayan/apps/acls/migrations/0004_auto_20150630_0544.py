# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acls', '0003_auto_20150630_0442'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='accesscontrollist',
            unique_together=set([('content_type', 'object_id', 'role')]),
        ),
    ]
