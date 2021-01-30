from datetime import datetime

from django.db import migrations
from django.utils.encoding import force_text
from django.utils.timezone import make_aware

from ..classes import GPGBackend


def operation_save_keys(apps, schema_editor):
    # Refill the creation and expiration fields with a date and time value.
    Key = apps.get_model(
        app_label='django_gpg', model_name='Key'
    )

    for key in Key.objects.using(alias=schema_editor.connection.alias).all():
        key_data = force_text(s=key.key_data)
        import_results, key_info = GPGBackend.get_instance().import_and_list_keys(
            key_data=key_data
        )

        key.creation_date = make_aware(
            value=datetime.fromtimestamp(int(key_info['date']))
        )
        if key_info['expires']:
            key.expiration_date = make_aware(
                value=datetime.fromtimestamp(
                    int(key_info['expires'])
                )
            )
        key.save()


def operation_save_keys_reverse(apps, schema_editor):
    # Remove the time component of the creation and expiration fields.
    Key = apps.get_model(
        app_label='django_gpg', model_name='Key'
    )

    for key in Key.objects.using(alias=schema_editor.connection.alias).all():
        key_data = force_text(s=key.key_data)
        import_results, key_info = GPGBackend.get_instance().import_and_list_keys(
            key_data=key_data
        )

        key.creation_date = make_aware(
            value=datetime.fromtimestamp(int(key_info['date']))
        ).date()
        if key_info['expires']:
            key.expiration_date = make_aware(
                value=datetime.fromtimestamp(
                    int(key_info['expires'])
                )
            ).date()
        key.save()


class Migration(migrations.Migration):
    """
    Known issue: Reverting this migration causes the key access to return the
    error:
    `invalid literal for int() with base 10: b'24 00:00:00'`
    as the date field tries to parse the unused time string fragment.
    There are no known solutions.
    Only workarounds is to execute the .save() method for each key to save
    the proper format value for the reverted date fields.
    2021-01-28 Django version 2.2.16. Mayan EDMS version 4.0.
    """
    dependencies = [
        ('django_gpg', '0007_auto_20210128_0504'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_save_keys,
            reverse_code=operation_save_keys_reverse
        ),
    ]
