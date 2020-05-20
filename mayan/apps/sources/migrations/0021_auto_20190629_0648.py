from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0020_auto_20181128_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailbasemodel',
            name='metadata_attachment_name',
            field=models.CharField(
                default='metadata.yaml', help_text='Name of the attachment '
                'that will contains the metadata type names and value '
                'pairs to be assigned to the rest of the downloaded '
                'attachments.', max_length=128,
                verbose_name='Metadata attachment name'
            ),
        ),
    ]
