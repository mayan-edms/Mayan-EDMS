from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_states', '0017_auto_20191213_0044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workflowtransitionfield',
            options={
                'verbose_name': 'Workflow transition field',
                'verbose_name_plural': 'Workflow transition fields'
            },
        ),
    ]
