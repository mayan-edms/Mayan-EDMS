import re

import django.core.validators
from django.db import migrations, models

import mayan.apps.converter.models
import mayan.apps.storage.classes


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0017_auto_20200810_0504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'label', models.CharField(
                        max_length=96, unique=True, verbose_name='Label'
                    )
                ),
                (
                    'internal_name', models.CharField(
                        db_index=True, help_text='This value will be '
                        'used when referencing this asset. Can only '
                        'contain letters, numbers, and underscores.',
                        max_length=255, unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[a-zA-Z0-9_]+\\Z'),
                                "Enter a valid 'internal name' consisting "
                                "of letters, numbers, and underscores.",
                                'invalid'
                            )
                        ], verbose_name='Internal name')
                ),
                (
                    'file', models.FileField(
                        storage=mayan.apps.storage.classes.DefinedStorageLazy(
                            name='converter__assets'
                        ), upload_to=mayan.apps.converter.models.upload_to,
                        verbose_name='File'
                    )
                ),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
                'ordering': ('label',),
            },
        ),
    ]
