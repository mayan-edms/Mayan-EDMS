from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0008_auto_20180310_1715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documenttypemetadatatype',
            options={
                'ordering': ('metadata_type',),
                'verbose_name': 'Document type metadata type options',
                'verbose_name_plural': 'Document type metadata types options'
            },
        ),
    ]
