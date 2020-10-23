from django.db import migrations

from ..layers import layer_saved_transformations


def code_copy_transformations(apps, schema_editor):
    ObjectLayer = apps.get_model(
        app_label='converter', model_name='ObjectLayer'
    )
    StoredLayer = apps.get_model(
        app_label='converter', model_name='StoredLayer'
    )
    Transformation = apps.get_model(
        app_label='converter', model_name='Transformation'
    )

    stored_layer, created = StoredLayer.objects.using(
        alias=schema_editor.connection.alias
    ).update_or_create(
        name=layer_saved_transformations.name, defaults={
            'order': layer_saved_transformations.order
        }
    )

    for transformation in Transformation.objects.using(alias=schema_editor.connection.alias).all():
        object_layer, created = ObjectLayer.objects.get_or_create(
            content_type=transformation.content_type,
            object_id=transformation.object_id,
            stored_layer=stored_layer
        )

        object_layer.transformations.create(
            order=transformation.order, name=transformation.name,
            arguments=transformation.arguments
        )


def code_copy_transformations_reverse(apps, schema_editor):
    LayerTransformation = apps.get_model(
        app_label='converter', model_name='LayerTransformation'
    )
    ObjectLayer = apps.get_model(
        app_label='converter', model_name='ObjectLayer'
    )
    StoredLayer = apps.get_model(
        app_label='converter', model_name='StoredLayer'
    )
    Transformation = apps.get_model(
        app_label='converter', model_name='Transformation'
    )

    stored_layer, created = StoredLayer.objects.using(
        alias=schema_editor.connection.alias
    ).update_or_create(
        name=layer_saved_transformations.name, defaults={
            'order': layer_saved_transformations.order
        }
    )

    for object_layer in ObjectLayer.objects.using(alias=schema_editor.connection.alias).filter(stored_layer=stored_layer):
        for layer_transformation in LayerTransformation.objects.using(alias=schema_editor.connection.alias).filter(object_layer=object_layer):
            Transformation.objects.using(alias=schema_editor.connection.alias).create(
                content_type=object_layer.content_type,
                object_id=object_layer.object_id,
                order=layer_transformation.order,
                name=layer_transformation.name,
                arguments=layer_transformation.arguments
            )


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0014_auto_20190814_0013'),
    ]

    operations = [
        migrations.RunPython(
            code=code_copy_transformations,
            reverse_code=code_copy_transformations_reverse
        )
    ]
