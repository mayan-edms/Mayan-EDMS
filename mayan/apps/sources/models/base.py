import json
import logging

from django.db import models, transaction
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from model_utils.managers import InheritanceManager

from mayan.apps.common.compressed_files import Archive
from mayan.apps.common.exceptions import NoMIMETypeMatch
from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.settings import setting_language

from ..literals import (
    DEFAULT_INTERVAL, SOURCE_CHOICES, SOURCE_UNCOMPRESS_CHOICES
)
from ..wizards import WizardStep

logger = logging.getLogger(name=__name__)


@python_2_unicode_compatible
class Source(models.Model):
    label = models.CharField(
        db_index=True, help_text=_('A short text to describe this source.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    objects = InheritanceManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

    def __str__(self):
        return '%s' % self.label

    @classmethod
    def class_fullname(cls):
        return force_text(dict(SOURCE_CHOICES).get(cls.source_type))

    def clean_up_upload_file(self, upload_file_object):
        pass
        # TODO: Should raise NotImplementedError?

    def fullname(self):
        return ' '.join([self.class_fullname(), '"%s"' % self.label])

    def handle_upload(
        self, file_object, description=None, document_type=None, expand=False,
        label=None, language=None, user=None
    ):
        """
        Handle an upload request from a file object which may be an individual
        document or a compressed file containing multiple documents.
        """
        documents = []
        if not document_type:
            document_type = self.document_type

        kwargs = {
            'description': description, 'document_type': document_type,
            'label': label, 'language': language, 'user': user
        }

        if expand:
            try:
                compressed_file = Archive.open(file_object=file_object)
                for compressed_file_child in compressed_file.members():
                    with compressed_file.open_member(filename=compressed_file_child) as file_object:
                        kwargs.update(
                            {'label': force_text(compressed_file_child)}
                        )
                        documents.append(
                            self.upload_document(
                                file_object=file_object, **kwargs
                            )
                        )
            except NoMIMETypeMatch:
                logger.debug(msg='Exception: NoMIMETypeMatch')
                documents.append(
                    self.upload_document(file_object=file_object, **kwargs)
                )
        else:
            documents.append(
                self.upload_document(file_object=file_object, **kwargs)
            )

        # Return a list of newly created documents. Used by the email source
        # to assign the from and subject metadata values.
        return documents

    def get_upload_file_object(self, form_data):
        pass
        # TODO: Should raise NotImplementedError?

    def upload_document(
        self, file_object, document_type, description=None, label=None,
        language=None, querystring=None, user=None
    ):
        """
        Upload an individual document
        """
        try:
            with transaction.atomic():
                document = Document(
                    description=description or '', document_type=document_type,
                    label=label or file_object.name,
                    language=language or setting_language.value
                )
                document.save(_user=user)
        except Exception as exception:
            logger.critical(
                'Unexpected exception while trying to create new document '
                '"%s" from source "%s"; %s',
                label or file_object.name, self, exception
            )
            raise
        else:
            try:
                document_version = document.new_version(
                    file_object=file_object, _user=user,
                )

                if user:
                    document.add_as_recent_document_for_user(user=user)

                layer_saved_transformations.copy_transformations(
                    source=self, targets=document_version.pages.all()
                )

            except Exception as exception:
                logger.critical(
                    'Unexpected exception while trying to create version for '
                    'new document "%s" from source "%s"; %s',
                    label or file_object.name, self, exception, exc_info=True
                )
                document.delete(to_trash=False)
                raise
            else:
                WizardStep.post_upload_process(
                    document=document, querystring=querystring
                )
                return document


class InteractiveSource(Source):
    objects = InheritanceManager()

    class Meta:
        verbose_name = _('Interactive source')
        verbose_name_plural = _('Interactive sources')


class OutOfProcessSource(Source):
    is_interactive = False

    objects = models.Manager()

    class Meta:
        verbose_name = _('Out of process')
        verbose_name_plural = _('Out of process')


class IntervalBaseModel(OutOfProcessSource):
    interval = models.PositiveIntegerField(
        default=DEFAULT_INTERVAL,
        help_text=_('Interval in seconds between checks for new documents.'),
        verbose_name=_('Interval')
    )
    document_type = models.ForeignKey(
        help_text=_(
            'Assign a document type to documents uploaded from this source.'
        ), on_delete=models.CASCADE, to=DocumentType,
        related_name='interval_sources', verbose_name=_('Document type')
    )
    uncompress = models.CharField(
        choices=SOURCE_UNCOMPRESS_CHOICES,
        help_text=_('Whether to expand or not, compressed archives.'),
        max_length=1, verbose_name=_('Uncompress')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('Interval source')
        verbose_name_plural = _('Interval sources')

    def _delete_periodic_task(self, pk=None):
        try:
            periodic_task = PeriodicTask.objects.get(
                name=self._get_periodic_task_name(pk=pk)
            )

            interval_instance = periodic_task.interval

            if tuple(interval_instance.periodictask_set.values_list('id', flat=True)) == (periodic_task.pk,):
                # Only delete the interval if nobody else is using it
                interval_instance.delete()
            else:
                periodic_task.delete()
        except PeriodicTask.DoesNotExist:
            logger.warning(
                'Tried to delete non existant periodic task "%s"',
                self._get_periodic_task_name(pk)
            )

    def _get_periodic_task_name(self, pk=None):
        return 'check_interval_source-%i' % (pk or self.pk)

    def delete(self, *args, **kwargs):
        pk = self.pk
        with transaction.atomic():
            super(IntervalBaseModel, self).delete(*args, **kwargs)
            self._delete_periodic_task(pk=pk)

    def save(self, *args, **kwargs):
        new_source = not self.pk
        with transaction.atomic():
            super(IntervalBaseModel, self).save(*args, **kwargs)

            if not new_source:
                self._delete_periodic_task()

            interval_instance, created = IntervalSchedule.objects.get_or_create(
                every=self.interval, period='seconds'
            )
            # Create a new interval or reuse someone else's
            PeriodicTask.objects.create(
                name=self._get_periodic_task_name(),
                interval=interval_instance,
                task='mayan.apps.sources.tasks.task_check_interval_source',
                kwargs=json.dumps(obj={'source_id': self.pk})
            )


class SourceLog(models.Model):
    source = models.ForeignKey(
        on_delete=models.CASCADE, related_name='logs', to=Source,
        verbose_name=_('Source')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_('Date time')
    )
    message = models.TextField(
        blank=True, editable=False, verbose_name=_('Message')
    )

    class Meta:
        get_latest_by = 'datetime'
        ordering = ('-datetime',)
        verbose_name = _('Log entry')
        verbose_name_plural = _('Log entries')
