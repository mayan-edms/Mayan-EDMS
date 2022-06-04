from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('quotas', '0001_initial')
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quota',
            options={
                'ordering': ('id',), 'verbose_name': 'Quota',
                'verbose_name_plural': 'Quotas'
            },
        )
    ]
