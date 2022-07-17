from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0008_auto_20180315_0029')
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objecteventsubscription',
            options={
                'ordering': ('pk',),
                'verbose_name': 'Object event subscription',
                'verbose_name_plural': 'Object event subscriptions'
            }
        )
    ]
