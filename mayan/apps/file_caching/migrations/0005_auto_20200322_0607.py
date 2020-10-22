from django.db import migrations
from django.utils.module_loading import import_string

STORAGE_PATH_UPDATE_MAP = {
    'mayan.apps.document_states.storages.storage_workflowimagecache': 'mayan.apps.document_states.storages.storage_workflow_image',
    'mayan.apps.documents.storages.storage_documentimagecache': 'mayan.apps.documents.storages.storage_document_image_cache'
}


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
    for cache in Cache.objects.using(alias=schema_editor.connection.alias).all():
        cache_storages[cache.pk] = import_string(
            dotted_path=cache.storage_instance_path
        ).get_storage_instance()

    for cache_partition_file in CachePartitionFile.objects.using(alias=schema_editor.connection.alias).all():
        cache_storages[
            cache_partition_file.partition.cache.pk
        ].delete(
            name='{}-{}'.format(
                cache_partition_file.partition.name,
                cache_partition_file.filename
            )
        )
        cache_partition_file.delete()

    CachePartition.objects.using(alias=schema_editor.connection.alias).all().delete()
    Cache.objects.using(alias=schema_editor.connection.alias).all().delete()


def operation_update_storage_paths(apps, schema_editor):
    Cache = apps.get_model(
        app_label='file_caching', model_name='Cache'
    )

    for cache in Cache.objects.using(alias=schema_editor.connection.alias).all():
        cache.storage_instance_path = STORAGE_PATH_UPDATE_MAP.get(
            cache.storage_instance_path, cache.storage_instance_path
        )
        cache.save()


def operation_update_storage_paths_reverse(apps, schema_editor):
    storage_path_update_map_inverted = {
        value: key for key, value in STORAGE_PATH_UPDATE_MAP.items()
    }

    Cache = apps.get_model(
        app_label='file_caching', model_name='Cache'
    )

    for cache in Cache.objects.using(alias=schema_editor.connection.alias).all():
        cache.storage_instance_path = storage_path_update_map_inverted.get(
            cache.storage_instance_path, cache.storage_instance_path
        )
        cache.save()


class Migration(migrations.Migration):
    dependencies = [
        ('file_caching', '0004_auto_20200309_0922'),
    ]
    operations = [
        migrations.RunPython(
            code=operation_update_storage_paths,
            reverse_code=operation_update_storage_paths_reverse
        ),
        migrations.RunPython(
            code=operation_purge_and_delete_caches,
            reverse_code=migrations.RunPython.noop
        ),
    ]
