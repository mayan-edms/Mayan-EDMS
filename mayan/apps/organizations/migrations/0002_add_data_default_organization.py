# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from ..literals import DEFAULT_ORGANIZATION_LABEL


def default_data(apps, schema_editor):
    # We can't import the Organization model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Organization = apps.get_model('organizations', 'Organization')
    default_organization = Organization(label=DEFAULT_ORGANIZATION_LABEL)
    default_organization.save()


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_data),
    ]
