from __future__ import absolute_import, unicode_literals

import logging
import uuid

from django.apps import apps
from django.core.files import File
from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _

from ..events import (
    event_document_create, event_document_properties_edit,
    event_document_type_change,
)
from ..literals import DOCUMENT_IMAGES_CACHE_NAME
from ..managers import DocumentManager, PassthroughManager, TrashCanManager
from ..settings import setting_language
from ..signals import post_document_type_change

from .document_type_models import DocumentType

__all__ = ('Document',)
logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Document(models.Model):
    """
    Defines a single document with it's fields and properties
    Fields:
    * uuid - UUID of a document, universally Unique ID. An unique identifier
    generated for each document. No two documents can ever have the same UUID.
    This ID is generated automatically.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text=_(
            'UUID of a document, universally Unique ID. An unique identifier '
            'generated for each document.'
        ), verbose_name=_('UUID')
    )
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='documents', to=DocumentType,
        verbose_name=_('Document type')
    )
    label = models.CharField(
        blank=True, db_index=True, default='', max_length=255,
        help_text=_('The name of the document.'), verbose_name=_('Label')
    )
    description = models.TextField(
        blank=True, default='', help_text=_(
            'An optional short text describing a document.'
        ), verbose_name=_('Description')
    )
    date_added = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text=_(
            'The server date and time when the document was finally '
            'processed and added to the system.'
        ), verbose_name=_('Added')
    )
    language = models.CharField(
        blank=True, default=setting_language.value, help_text=_(
            'The dominant language in the document.'
        ), max_length=8, verbose_name=_('Language')
    )
    in_trash = models.BooleanField(
        db_index=True, default=False, help_text=_(
            'Whether or not this document is in the trash.'
        ), editable=False, verbose_name=_('In trash?')
    )
    # TODO: set editable to False
    deleted_date_time = models.DateTimeField(
        blank=True, editable=True, help_text=_(
            'The server date and time when the document was moved to the '
            'trash.'
        ), null=True, verbose_name=_('Date and time trashed')
    )
    is_stub = models.BooleanField(
        db_index=True, default=True, editable=False, help_text=_(
            'A document stub is a document with an entry on the database but '
            'no file uploaded. This could be an interrupted upload or a '
            'deferred upload via the API.'
        ), verbose_name=_('Is stub?')
    )

    objects = DocumentManager()
    passthrough = PassthroughManager()
    trash = TrashCanManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def __str__(self):
        return self.label or ugettext('Document stub, id: %d') % self.pk

    def add_as_recent_document_for_user(self, user):
        RecentDocument = apps.get_model(
            app_label='documents', model_name='RecentDocument'
        )
        return RecentDocument.objects.add_document_for_user(user, self)

    @cached_property
    def cache(self):
        Cache = apps.get_model(app_label='file_caching', model_name='Cache')
        return Cache.objects.get(name=DOCUMENT_IMAGES_CACHE_NAME)

    @cached_property
    def cache_partition(self):
        partition, created = self.cache.partitions.get_or_create(
            name='document-{}'.format(self.uuid)
        )
        return partition

    @property
    def checksum(self):
        return self.latest_version.checksum

    @property
    def date_updated(self):
        return self.latest_version.timestamp

    def delete(self, *args, **kwargs):
        to_trash = kwargs.pop('to_trash', True)

        if not self.in_trash and to_trash:
            self.in_trash = True
            self.deleted_date_time = now()
            self.save()
        else:
            for version in self.versions.all():
                version.delete()

            return super(Document, self).delete(*args, **kwargs)

    def exists(self):
        """
        Returns a boolean value that indicates if the document's
        latest version file exists in storage
        """
        latest_version = self.latest_version
        if latest_version:
            return latest_version.exists()
        else:
            return False

    @property
    def file_mime_encoding(self):
        return self.latest_version.encoding

    @property
    def file_mimetype(self):
        return self.latest_version.mimetype

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_preview', kwargs={'pk': self.pk}
        )

    def get_api_image_url(self, *args, **kwargs):
        first_page = self.pages.first()
        if first_page:
            return first_page.get_api_image_url(*args, **kwargs)

    @property
    def is_in_trash(self):
        return self.in_trash

    @property
    def latest_version(self):
        return self.versions.order_by('timestamp').last()

    def natural_key(self):
        return (self.uuid,)
    natural_key.dependencies = ['documents.DocumentType']

    def new_version(self, file_object, append_pages=False, comment=None, _user=None):
        logger.info('Creating new document version for document: %s', self)
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        document_version = DocumentVersion(
            document=self, comment=comment or '', file=File(file_object)
        )
        document_version.save(append_pages=append_pages, _user=_user)

        logger.info('New document version queued for document: %s', self)

        return document_version

    def open(self, *args, **kwargs):
        """
        Return a file descriptor to a document's file irrespective of
        the storage backend
        """
        return self.latest_version.open(*args, **kwargs)

    @property
    def page_count(self):
        return self.pages.count()

    @property
    def pages(self):
        return self.pages.all()

    @property
    def pages_all(self):
        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )
        return DocumentPage.passthrough.filter(document=self)

    def pages_reset(self, update_page_count=True):
        with transaction.atomic():
            for page in self.pages.all():
                page.delete()

            if update_page_count:
                self.latest_version.update_page_count()

            for version_page in self.latest_version.pages.all():
                self.pages.create(
                    content_object=version_page
                )

    def restore(self):
        self.in_trash = False
        self.save()

    def save(self, *args, **kwargs):
        user = kwargs.pop('_user', None)
        _commit_events = kwargs.pop('_commit_events', True)
        new_document = not self.pk
        super(Document, self).save(*args, **kwargs)

        if new_document:
            if user:
                self.add_as_recent_document_for_user(user)
                event_document_create.commit(
                    actor=user, target=self, action_object=self.document_type
                )
            else:
                event_document_create.commit(
                    target=self, action_object=self.document_type
                )
        else:
            if _commit_events:
                event_document_properties_edit.commit(actor=user, target=self)

    def save_to_file(self, *args, **kwargs):
        return self.latest_version.save_to_file(*args, **kwargs)

    def set_document_type(self, document_type, force=False, _user=None):
        has_changed = self.document_type != document_type

        self.document_type = document_type
        self.save()
        if has_changed or force:
            post_document_type_change.send(
                sender=self.__class__, instance=self
            )

            event_document_type_change.commit(actor=_user, target=self)
            if _user:
                self.add_as_recent_document_for_user(user=_user)

    @property
    def size(self):
        return self.latest_version.size
