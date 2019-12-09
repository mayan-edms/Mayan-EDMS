from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0050_auto_20190725_0451'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentpage',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled'),
        ),
    ]
