from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('file_caching', '0008_auto_20210426_0717')
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cache',
            options={
                'ordering': ('id',), 'verbose_name': 'Cache',
                'verbose_name_plural': 'Caches'
            }
        )
    ]
