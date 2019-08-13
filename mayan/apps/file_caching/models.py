from __future__ import unicode_literals

from contextlib import contextmanager
import logging

from django.core.files.base import ContentFile
from django.db import models, transaction
from django.db.models import Sum
from django.template.defaultfilters import filesizeformat
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.lock_manager.exceptions import LockError
from mayan.apps.lock_manager.runtime import locking_backend

from .events import (
    event_cache_created, event_cache_edited, event_cache_purged
)

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Cache(models.Model):
    name = models.CharField(
        help_text=_('Internal name of the cache.'), max_length=128,
        unique=True, verbose_name=_('Name')
    )
    label = models.CharField(
        help_text=_('A short text describing the cache.'), max_length=128,
        verbose_name=_('Label')
    )
    maximum_size = models.PositiveIntegerField(
        help_text=_('Maximum size of the cache in bytes.'),
        verbose_name=_('Maximum size')
    )
    storage_instance_path = models.CharField(
        help_text=_(
            'Dotted path to the actual storage class used for the cache.'
        ), max_length=255, unique=True, verbose_name=_('Storage instance path')
    )

    class Meta:
        verbose_name = _('Cache')
        verbose_name_plural = _('Caches')

    def __str__(self):
        return self.label

    def get_files(self):
        return CachePartitionFile.objects.filter(partition__cache__id=self.pk)

    def get_maximum_size_display(self):
        return filesizeformat(bytes_=self.maximum_size)

    get_maximum_size_display.short_description = _('Maximum size')

    def get_total_size(self):
        """
        Return the actual usage of the cache.
        """
        return self.get_files().aggregate(
            file_size__sum=Sum('file_size')
        )['file_size__sum'] or 0

    def get_total_size_display(self):
        return filesizeformat(bytes_=self.get_total_size())

    get_total_size_display.short_description = _('Total size')

    def prune(self):
        """
        Deletes files until the total size of the cache is below the allowed
        maximum size of the cache.
        """
        while self.get_total_size() > self.maximum_size:
            self.get_files().earliest().delete()

    def purge(self, _user=None):
        """
        Deletes the entire cache.
        """
        for partition in self.partitions.all():
            partition.purge()

        event_cache_purged.commit(actor=_user, target=self)

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)
        with transaction.atomic():
            is_new = not self.pk
            result = super(Cache, self).save(*args, **kwargs)
            if is_new:
                event_cache_created.commit(
                    actor=_user, target=self
                )
            else:
                event_cache_edited.commit(
                    actor=_user, target=self
                )

        self.prune()
        return result

    @cached_property
    def storage(self):
        return import_string(self.storage_instance_path)


class CachePartition(models.Model):
    cache = models.ForeignKey(
        on_delete=models.CASCADE, related_name='partitions',
        to=Cache, verbose_name=_('Cache')
    )
    name = models.CharField(
        max_length=128, verbose_name=_('Name')
    )

    class Meta:
        unique_together = ('cache', 'name')
        verbose_name = _('Cache partition')
        verbose_name_plural = _('Cache partitions')

    @staticmethod
    def get_combined_filename(parent, filename):
        return '{}-{}'.format(parent, filename)

    @contextmanager
    def create_file(self, filename):
        lock_id = 'cache_partition-create_file-{}-{}'.format(self.pk, filename)
        try:
            logger.debug('trying to acquire lock: %s', lock_id)
            lock = locking_backend.acquire_lock(lock_id)
            logger.debug('acquired lock: %s', lock_id)
            try:
                self.cache.prune()

                # Since open "wb+" doesn't create files force the creation of an
                # empty file.
                self.cache.storage.delete(
                    name=self.get_full_filename(filename=filename)
                )
                self.cache.storage.save(
                    name=self.get_full_filename(filename=filename),
                    content=ContentFile(content='')
                )

                try:
                    with transaction.atomic():
                        partition_file = self.files.create(filename=filename)
                        yield partition_file.open(mode='wb')
                        partition_file.update_size()
                except Exception as exception:
                    logger.error(
                        'Unexpected exception while trying to save new '
                        'cache file; %s', exception
                    )
                    self.cache.storage.delete(
                        name=self.get_full_filename(filename=filename)
                    )
                    raise
            finally:
                lock.release()
        except LockError:
            logger.debug('unable to obtain lock: %s' % lock_id)
            raise

    def delete(self, *args, **kwargs):
        self.purge()
        return super(CachePartition, self).delete(*args, **kwargs)

    def get_file(self, filename):
        try:
            return self.files.get(filename=filename)
        except self.files.model.DoesNotExist:
            return None

    def get_full_filename(self, filename):
        return CachePartition.get_combined_filename(
            parent=self.name, filename=filename
        )

    def purge(self):
        for parition_file in self.files.all():
            parition_file.delete()


class CachePartitionFile(models.Model):
    partition = models.ForeignKey(
        on_delete=models.CASCADE, related_name='files',
        to=CachePartition, verbose_name=_('Cache partition')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Date time')
    )
    filename = models.CharField(max_length=255, verbose_name=_('Filename'))
    file_size = models.PositiveIntegerField(
        default=0, verbose_name=_('File size')
    )

    class Meta:
        get_latest_by = 'datetime'
        unique_together = ('partition', 'filename')
        verbose_name = _('Cache partition file')
        verbose_name_plural = _('Cache partition files')

    def delete(self, *args, **kwargs):
        self.partition.cache.storage.delete(name=self.full_filename)
        return super(CachePartitionFile, self).delete(*args, **kwargs)

    def exists(self):
        return self.partition.cache.storage.exists(name=self.full_filename)

    @cached_property
    def full_filename(self):
        return CachePartition.get_combined_filename(
            parent=self.partition.name, filename=self.filename
        )

    def open(self, mode='rb'):
        # Open the file for reading. If the file is written to, the
        # .update_size() must be called.
        try:
            return self.partition.cache.storage.open(
                name=self.full_filename, mode=mode
            )
        except Exception as exception:
            logger.error(
                'Unexpected exception opening the cache file; %s', exception
            )
            raise

    def update_size(self):
        self.file_size = self.partition.cache.storage.size(
            name=self.full_filename
        )
        self.save()
