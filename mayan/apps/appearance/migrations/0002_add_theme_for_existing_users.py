from django.conf import settings
from django.db import migrations


def code_add_user_theme_settings_to_existing_users(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    UserThemeSetting = apps.get_model(
        app_label='appearance', model_name='UserThemeSetting'
    )

    for user in User.objects.using(alias=schema_editor.connection.alias).all():
        UserThemeSetting.objects.using(
            alias=schema_editor.connection.alias
        ).create(user=user)


def code_remove_user_theme_settings_from_existing_users(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    UserThemeSetting = apps.get_model(
        app_label='appearance', model_name='UserThemeSetting'
    )

    for user in User.objects.using(alias=schema_editor.connection.alias).all():
        UserThemeSetting.objects.using(
            alias=schema_editor.connection.alias
        ).filter(user=user).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('appearance', '0001_initial')
    ]

    operations = [
        migrations.RunPython(
            code=code_add_user_theme_settings_to_existing_users,
            reverse_code=code_remove_user_theme_settings_from_existing_users
        )
    ]
