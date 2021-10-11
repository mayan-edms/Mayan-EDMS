from django.db import migrations


def code_delete_index_instance_nodes(apps, schema_editor):
    IndexInstanceNode = apps.get_model(
        app_label='document_indexing', model_name='IndexInstanceNode'
    )

    IndexInstanceNode.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0022_indexinstance'),
    ]

    operations = [
        migrations.RunPython(
            code=code_delete_index_instance_nodes,
            reverse_code=migrations.RunPython.noop
        ),
    ]
