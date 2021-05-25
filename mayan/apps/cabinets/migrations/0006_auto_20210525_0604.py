from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cabinets', '0005_auto_20210525_0500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cabinet',
            options={
                'verbose_name': 'Cabinet', 'verbose_name_plural': 'Cabinets'
            },
        ),
    ]
