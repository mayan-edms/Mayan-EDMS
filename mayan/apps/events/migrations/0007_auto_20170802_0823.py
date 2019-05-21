from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_objecteventsubscription'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={
                'ordering': ('-action__timestamp',),
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications'
            },
        ),
    ]
