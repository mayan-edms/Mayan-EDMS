from django.db import migrations

from ..classes import DuplicateBackend


def operation_initialize_stored_backend_model(apps, schema_editor):
    StoredDuplicateBackend = apps.get_model(
        app_label='duplicates', model_name='StoredDuplicateBackend'
    )

    for backend_path, backend_class in DuplicateBackend.get_all():
        stored_backend, created = StoredDuplicateBackend.objects.using(
            alias=schema_editor.connection.alias
        ).get_or_create(
            backend_path=backend_path
        )


def operation_initialize_stored_backend_model_reverse(apps, schema_editor):
    StoredDuplicateBackend = apps.get_model(
        app_label='duplicates', model_name='StoredDuplicateBackend'
    )

    for stored_backend in StoredDuplicateBackend.objects.using(
        alias=schema_editor.connection.alias
    ).all():
        stored_backend.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('duplicates', '0004_storedduplicatebackend'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_initialize_stored_backend_model,
            reverse_code=migrations.RunPython.noop
        ),
    ]
