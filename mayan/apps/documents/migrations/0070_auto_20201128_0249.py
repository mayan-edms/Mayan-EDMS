from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0069_auto_20201128_0247'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecentDocument',
            new_name='RecentlyAccessedDocument',
        ),
    ]
