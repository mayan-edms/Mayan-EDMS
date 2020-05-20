from django.db import migrations
from django.template.defaultfilters import slugify


def operation_assign_slugs(apps, schema_editor):
    Index = apps.get_model(app_label='document_indexing', model_name='Index')

    for index in Index.objects.using(schema_editor.connection.alias).all():
        index.slug = slugify(index.label)
        index.save()


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0005_index_slug'),
    ]

    operations = [
        migrations.RunPython(code=operation_assign_slugs),
    ]
