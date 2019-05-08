from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acls', '0002_auto_20150703_0513'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesscontrollist',
            options={
                'ordering': ('pk',), 'verbose_name': 'Access entry',
                'verbose_name_plural': 'Access entries'
            },
        ),
    ]
