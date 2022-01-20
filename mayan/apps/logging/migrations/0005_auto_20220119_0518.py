from django.db import migrations


def code_delete_all_error_log_partitions(apps, schema_editor):
    ErrorLogPartition = apps.get_model(
        app_label='logging', model_name='ErrorLogPartition'
    )

    ErrorLogPartition.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('logging', '0004_auto_20220118_2327'),
    ]

    operations = [
        migrations.RunPython(
            code=code_delete_all_error_log_partitions,
            reverse_code=migrations.RunPython.noop
        )
    ]
