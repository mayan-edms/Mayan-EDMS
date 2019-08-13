from __future__ import unicode_literals

from django.db import migrations

from ..storages import storage_documentimagecache


def operation_clear_old_cache(apps, schema_editor):
    DocumentPageCachedImage = apps.get_model(
        'documents', 'DocumentPageCachedImage'
    )

    for cached_image in DocumentPageCachedImage.objects.using(schema_editor.connection.alias).all():
        # Delete each cached image directly since the model doesn't exists and
        # will not trigger the physical deletion of the stored file
        storage_documentimagecache.delete(cached_image.filename)
        cached_image.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0048_auto_20190711_0544'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_clear_old_cache,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name='documentpagecachedimage',
            name='document_page',
        ),
        migrations.DeleteModel(
            name='DocumentPageCachedImage',
        ),
    ]
