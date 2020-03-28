# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0022_auto_20191022_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailbasemodel',
            name='from_metadata_type',
            field=models.ForeignKey(
                blank=True, help_text='Select a metadata type to store '
                'the email\'s "from" value. Must be a valid metadata type '
                'for the document type selected previously.', null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='email_from', to='metadata.MetadataType',
                verbose_name='From metadata type'
            ),
        ),
        migrations.AlterField(
            model_name='emailbasemodel',
            name='subject_metadata_type',
            field=models.ForeignKey(
                blank=True, help_text="Select a metadata type to store "
                "the email's subject value. Must be a valid metadata type "
                "for the document type selected previously.", null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='email_subject', to='metadata.MetadataType',
                verbose_name='Subject metadata type'
            ),
        ),
        migrations.AlterField(
            model_name='source',
            name='label',
            field=models.CharField(
                db_index=True, help_text='A short text to describe this '
                'source.', max_length=128, unique=True, verbose_name='Label'
            ),
        ),
    ]
