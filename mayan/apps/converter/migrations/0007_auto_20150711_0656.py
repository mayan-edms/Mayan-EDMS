from django.db import models, migrations

import mayan.apps.common.validators


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0006_auto_20150708_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transformation',
            name='arguments',
            field=models.TextField(
                help_text='Enter the arguments for the transformation as a '
                'YAML dictionary. ie: {"degrees": 180}', blank=True,
                verbose_name='Arguments',
                validators=[mayan.apps.common.validators.YAMLValidator()]
            ),
            preserve_default=True,
        ),
    ]
