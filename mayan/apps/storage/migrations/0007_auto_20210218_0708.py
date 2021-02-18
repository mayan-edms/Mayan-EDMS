from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('storage', '0006_auto_20201024_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='downloadfile',
            options={
                'ordering': ('-datetime',), 'verbose_name': 'Download file',
                'verbose_name_plural': 'Download files'
            },
        ),
    ]
