from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0025_auto_20211201_0842')
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indexinstancenode',
            options={
                'ordering': ('value',),
                'verbose_name': 'Index instance node',
                'verbose_name_plural': 'Indexes instances node'
            }
        )
    ]
