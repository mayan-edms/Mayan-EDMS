from django.db import migrations


def code_revert_module_paths(apps, schema_editor):
    MetadataType = apps.get_model(
        app_label='metadata', model_name='MetadataType'
    )

    for metadata_type in MetadataType.objects.all():
        metadata_type.parser = metadata_type.parser.replace(
            'mayan.apps.metadata.metadata_parsers',
            'mayan.apps.metadata.parsers'
        )
        metadata_type.validation = metadata_type.validation.replace(
            'mayan.apps.metadata.metadata_validators',
            'mayan.apps.metadata.validators'
        )
        metadata_type.save()


def code_update_module_paths(apps, schema_editor):
    MetadataType = apps.get_model(
        app_label='metadata', model_name='MetadataType'
    )

    for metadata_type in MetadataType.objects.all():
        metadata_type.parser = metadata_type.parser.replace(
            'mayan.apps.metadata.parsers',
            'mayan.apps.metadata.metadata_parsers'
        )
        metadata_type.validation = metadata_type.validation.replace(
            'mayan.apps.metadata.validators',
            'mayan.apps.metadata.metadata_validators'
        )
        metadata_type.save()


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0015_metadatatype_validation_arguments')
    ]

    operations = [
        migrations.RunPython(
            code=code_update_module_paths,
            reverse_code=code_revert_module_paths
        )
    ]
