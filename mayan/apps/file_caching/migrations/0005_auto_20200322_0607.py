from django.db import migrations
from django.utils.module_loading import import_string


def operation_purge_and_delete_caches(apps, schema_editor):
    Cache = apps.get_model(
        app_label='file_caching', model_name='Cache'
    )
    CachePartition = apps.get_model(
        app_label='file_caching', model_name='CachePartition'
    )
    CachePartitionFile = apps.get_model(
        app_label='file_caching', model_name='CachePartitionFile'
    )

    cache_storages = {}
    for cache in Cache.objects.using(schema_editor.connection.alias).all():
        cache_storages[cache.pk] = import_string(dotted_path=cache.storage_instance_path)

    for cache_partition_file in CachePartitionFile.objects.using(schema_editor.connection.alias).all():
        cache_storages[
            cache_partition_file.partition.cache.pk
        ].delete(
            name='{}-{}'.format(
                cache_partition_file.partition.name,
                cache_partition_file.filename
            )
        )
        cache_partition_file.delete()

    for cache_partition in CachePartition.objects.using(schema_editor.connection.alias).all():
        cache_partition.delete()

    for cache in Cache.objects.using(schema_editor.connection.alias).all():
        cache.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('file_caching', '0004_auto_20200309_0922'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_purge_and_delete_caches,
            reverse_code=migrations.RunPython.noop
        ),
    ]
