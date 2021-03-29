import logging

from django.core.files.storage import Storage
from django.db import migrations
from django.utils.module_loading import import_string

STORAGE_PATH_UPDATE_MAP = {
    'mayan.apps.document_states.storages.storage_workflowimagecache': 'mayan.apps.document_states.storages.storage_workflow_image',
    'mayan.apps.documents.storages.storage_documentimagecache': 'mayan.apps.documents.storages.storage_document_image_cache'
}
logger = logging.getLogger(name=__name__)


class DummyStorage(Storage):
    def delete(self, name):
        """
        Do nothing. This dummy storage avoids an if in the
        `cache_partition_file` loop.
        """


def operation_purge_and_delete_caches(apps, schema_editor):
    Cache = apps.get_model(
        app_label='file_caching', model_name='Cache'
    )
    CachePartitionFile = apps.get_model(
        app_label='file_caching', model_name='CachePartitionFile'
    )

    cursor_primary = schema_editor.connection.create_cursor(
        name='file_caching_partition_files'
    )
    cursor_secondary = schema_editor.connection.cursor()

    query = str(
        CachePartitionFile.objects.values(
            'partition__name', 'filename', 'partition__cache_id'
        ).query
    )

    '''
    Expected resulting query:
        SELECT
            "file_caching_cachepartition"."name",
            "file_caching_cachepartitionfile"."filename",
            "file_caching_cachepartition"."cache_id"
        FROM "file_caching_cachepartitionfile"
        INNER JOIN
            "file_caching_cachepartition" ON (
                "file_caching_cachepartitionfile"."partition_id" = "file_caching_cachepartition"."id"
            )
    '''

    cache_storages = {}
    for cache in Cache.objects.using(alias=schema_editor.connection.alias).all():
        try:
            cache_storages[cache.pk] = import_string(
                dotted_path=cache.storage_instance_path
            ).get_storage_instance()
        except ImportError as exception:
            logger.error(
                'Storage "%s" not found. Remove the files from this '
                'storage manually.; %s', cache.storage_instance_path,
                exception
            )
            cache_storages[cache.pk] = DummyStorage()

    cursor_primary.execute(query=query)
    for partition_name, filename, cache_id in cursor_primary.fetchall():
        cache_storages[
            cache_id
        ].delete(
            name='{}-{}'.format(
                partition_name,
                filename
            )
        )

    table_names = (
        'file_caching_cachepartitionfile', 'file_caching_cachepartition',
        'file_caching_cache'
    )

    for table_name in table_names:
        cursor_secondary.execute(
            sql='DELETE FROM {};'.format(
                schema_editor.connection.ops.quote_name(
                    name=table_name
                )
            )
        )


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
