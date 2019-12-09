from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_caching', '0002_auto_20190729_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cache',
            name='name',
            field=models.CharField(
                db_index=True, help_text='Internal name of the cache.',
                max_length=128, unique=True, verbose_name='Name'
            ),
        ),
    ]
