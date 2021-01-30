from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locales', '0002_auto_20210130_0324'),
        ('common', '0018_delete_userlocaleprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserLocaleProfileNew',
            new_name='UserLocaleProfile',
        ),
    ]
