from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0006_documenttag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={
                'ordering': ('label',), 'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags'
            },
        ),
    ]
