from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0006_newversionblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentcheckout',
            options={
                'ordering': ('pk',), 'verbose_name': 'Document checkout',
                'verbose_name_plural': 'Document checkouts'
            },
        ),
    ]
