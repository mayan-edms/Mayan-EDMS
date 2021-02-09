from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0007_auto_20150918_0800'),
        ('sources', '0008_auto_20150815_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailbasemodel',
            name='from_metadata_type',
            field=models.ForeignKey(
                blank=True,
                help_text='Select a metadata type valid for the document '
                'type selected in which to store the email\'s "from" value.',
                null=True, on_delete=models.CASCADE,
                related_name='email_from', to='metadata.MetadataType',
                verbose_name='From metadata type'
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailbasemodel',
            name='subject_metadata_type',
            field=models.ForeignKey(
                blank=True, on_delete=models.CASCADE,
                related_name='email_subject',
                help_text='Select a metadata '
                'type valid for the document type selected in which to '
                'store the email\'s subject.',
                null=True, to='metadata.MetadataType',
                verbose_name='Subject metadata type'
            ),
            preserve_default=True,
        ),
    ]
