import logging

from django.db import migrations

from mayan.apps.storage.utils import get_storage_subclass

from ..settings import (
    setting_document_file_page_image_cache_storage_backend,
    setting_document_file_page_image_cache_storage_backend_arguments,
)

logger = logging.getLogger(name=__name__)


def operation_clear_old_cache(apps, schema_editor):
    try:
        storage_documentimagecache = get_storage_subclass(
            dotted_path=setting_document_file_page_image_cache_storage_backend.value
        )(**setting_document_file_page_image_cache_storage_backend_arguments.value)
    except Exception as exception:
        message = (
            'Unable to initialize the document image cache storage. '
            'Check the settings {} and {} for formatting errors.'.format(
                setting_document_file_page_image_cache_storage_backend.global_name,
                setting_document_file_page_image_cache_storage_backend_arguments.global_name
            )
        )

        logger.fatal(message)
        raise TypeError(message) from exception

    DocumentPageCachedImage = apps.get_model(
        app_label='documents', model_name='DocumentPageCachedImage'
    )

    for cached_image in DocumentPageCachedImage.objects.using(alias=schema_editor.connection.alias).all():
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
