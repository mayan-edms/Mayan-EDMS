from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0007_auto_20150918_0800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentmetadata',
            options={
                'ordering': ('metadata_type',),
                'verbose_name': 'Document metadata',
                'verbose_name_plural': 'Document metadata'
            },
        ),
    ]
