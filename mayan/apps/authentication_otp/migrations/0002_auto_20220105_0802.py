from django.conf import settings
from django.db import migrations


def code_user_otp_data_initialize(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    UserOTPData = apps.get_model(
        app_label='authentication_otp', model_name='UserOTPData'
    )

    for user in User.objects.using(alias=schema_editor.connection.alias).all():
        UserOTPData.objects.using(
            alias=schema_editor.connection.alias
        ).get_or_create(user=user)


class Migration(migrations.Migration):
    dependencies = [
        ('authentication_otp', '0001_initial')
    ]

    operations = [
        migrations.RunPython(code=code_user_otp_data_initialize)
    ]
