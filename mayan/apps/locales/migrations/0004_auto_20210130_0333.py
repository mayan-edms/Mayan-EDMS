from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('locales', '0003_auto_20210130_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocaleprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='locale_profile', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
