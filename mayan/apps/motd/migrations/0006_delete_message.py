from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('announcements', '0002_auto_20210212_1022'),
        ('motd', '0005_auto_20160510_0025'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
