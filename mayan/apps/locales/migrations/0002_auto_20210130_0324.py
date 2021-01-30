from django.db import migrations


def code_copy_locales(apps, schema_editor):
    UserLocaleProfile = apps.get_model(
        app_label='common', model_name='UserLocaleProfile'
    )
    UserLocaleProfileNew = apps.get_model(
        app_label='locales', model_name='UserLocaleProfileNew'
    )

    for locale_profile in UserLocaleProfile.objects.using(alias=schema_editor.connection.alias):
        UserLocaleProfileNew.objects.create(
            user=locale_profile.user,
            timezone=locale_profile.timezone,
            language=locale_profile.language
        )


def code_copy_locales_reverse(apps, schema_editor):
    UserLocaleProfile = apps.get_model(
        app_label='common', model_name='UserLocaleProfile'
    )
    UserLocaleProfileNew = apps.get_model(
        app_label='locales', model_name='UserLocaleProfileNew'
    )

    for locale_profile in UserLocaleProfileNew.objects.using(alias=schema_editor.connection.alias):
        UserLocaleProfile.objects.create(
            user=locale_profile.user,
            timezone=locale_profile.timezone,
            language=locale_profile.language
        )


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0015_auto_20200501_0631'),
        ('locales', '0001_initial')
    ]

    operations = [
        migrations.RunPython(
            code=code_copy_locales,
            reverse_code=code_copy_locales_reverse,
        ),
    ]

    run_before = [
        ('common', '0018_delete_userlocaleprofile'),
    ]
