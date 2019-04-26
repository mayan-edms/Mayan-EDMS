from __future__ import unicode_literals

from datetime import timedelta
import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Max
from django.utils.encoding import force_text
from django.utils.timezone import now

from .literals import STUB_EXPIRATION_INTERVAL
from .settings import setting_favorite_count, setting_recent_access_count

logger = logging.getLogger(__name__)


class DocumentManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.model.passthrough.get(uuid=force_text(uuid))

    def get_queryset(self):
        return TrashCanQuerySet(
            self.model, using=self._db
        ).filter(in_trash=False).filter(is_stub=False)

    def invalidate_cache(self):
        for document in self.model.objects.all():
            document.invalidate_cache()


class DocumentPageCachedImage(models.Manager):
    def get_by_natural_key(self, filename, document_page_natural_key):
        DocumentPage = apps.get_model(
            app_label='documents', model_name='DocumentPage'
        )
        try:
            document_page = DocumentPage.objects.get_by_natural_key(
                *document_page_natural_key
            )
        except DocumentPage.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document_page__pk=document_page.pk, filename=filename)


class DocumentPageManager(models.Manager):
    def get_by_natural_key(self, page_number, document_version_natural_key):
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )
        try:
            document_version = DocumentVersion.objects.get_by_natural_key(*document_version_natural_key)
        except DocumentVersion.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document_version__pk=document_version.pk, page_number=page_number)


class DocumentTypeManager(models.Manager):
    def check_delete_periods(self):
        logger.info(msg='Executing')

        for document_type in self.all():
            logger.info(
                'Checking deletion period of document type: %s', document_type
            )
            if document_type.delete_time_period and document_type.delete_time_unit:
                delta = timedelta(
                    **{
                        document_type.delete_time_unit: document_type.delete_time_period
                    }
                )
                logger.info(
                    'Document type: %s, has a deletion period delta of: %s',
                    document_type, delta
                )
                for document in document_type.deleted_documents.filter(deleted_date_time__lt=now() - delta):
                    logger.info(
                        'Document "%s" with id: %d, trashed on: %s, exceded '
                        'delete period', document, document.pk,
                        document.deleted_date_time
                    )
                    document.delete()
            else:
                logger.info(
                    'Document type: %s, has a no retention delta', document_type
                )

        logger.info(msg='Finshed')

    def check_trash_periods(self):
        logger.info(msg='Executing')

        for document_type in self.all():
            logger.info(
                'Checking trash period of document type: %s', document_type
            )
            if document_type.trash_time_period and document_type.trash_time_unit:
                delta = timedelta(
                    **{
                        document_type.trash_time_unit: document_type.trash_time_period
                    }
                )
                logger.info(
                    'Document type: %s, has a trash period delta of: %s',
                    document_type, delta
                )
                for document in document_type.documents.filter(date_added__lt=now() - delta):
                    logger.info(
                        'Document "%s" with id: %d, added on: %s, exceded '
                        'trash period', document, document.pk,
                        document.date_added
                    )
                    document.delete()
            else:
                logger.info(
                    'Document type: %s, has a no retention delta', document_type
                )

        logger.info(msg='Finshed')

    def get_by_natural_key(self, label):
        return self.get(label=label)


class DocumentVersionManager(models.Manager):
    def get_by_natural_key(self, checksum, document_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        try:
            document = Document.objects.get_by_natural_key(*document_natural_key)
        except Document.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document__pk=document.pk, checksum=checksum)


class DuplicatedDocumentManager(models.Manager):
    def clean_empty_duplicate_lists(self):
        self.filter(documents=None).delete()

    def get_duplicated_documents(self):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        return Document.objects.filter(
            pk__in=self.filter(documents__isnull=False).values_list(
                'document_id', flat=True
            )
        )

    def scan(self):
        """
        Find duplicates by iterating over all documents and then
        find matching latest version checksums
        """
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        for document in Document.objects.all():
            self.scan_for(document=document, scan_children=False)

    def scan_for(self, document, scan_children=True):
        """
        Find duplicates by matching latest version checksums
        """
        if not document.latest_version:
            return None

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        # Get the documents whose latest version matches the checksum
        # of the current document and exclude the current document
        duplicates = Document.objects.annotate(
            max_timestamp=Max('versions__timestamp')
        ).filter(
            versions__timestamp=F('max_timestamp'),
            versions__checksum=document.checksum
        ).exclude(pk=document.pk)

        if duplicates.exists():
            instance, created = self.get_or_create(document=document)
            instance.documents.add(*duplicates)
        else:
            self.filter(document=document).delete()

        if scan_children:
            for document in duplicates:
                self.scan_for(document=document, scan_children=False)


class FavoriteDocumentManager(models.Manager):
    def add_for_user(self, user, document):
        favorite_document, created = self.model.objects.get_or_create(
            user=user, document=document
        )

        old_favorites_to_delete = self.filter(user=user).values_list('pk', flat=True)[setting_favorite_count.value:]
        self.filter(pk__in=list(old_favorites_to_delete)).delete()

    def get_by_natural_key(self, datetime_accessed, document_natural_key, user_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        User = get_user_model()
        try:
            document = Document.objects.get_by_natural_key(*document_natural_key)
        except Document.DoesNotExist:
            raise self.model.DoesNotExist
        else:
            try:
                user = User.objects.get_by_natural_key(*user_natural_key)
            except User.DoesNotExist:
                raise self.model.DoesNotExist

        return self.get(document__pk=document.pk, user__pk=user.pk)

    def get_for_user(self, user):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        return Document.objects.filter(favorites__user=user)

    def remove_for_user(self, user, document):
        self.get(user=user, document=document).delete()


class PassthroughManager(models.Manager):
    def delete_stubs(self):
        for stale_stub_document in self.filter(is_stub=True, date_added__lt=now() - timedelta(seconds=STUB_EXPIRATION_INTERVAL)):
            stale_stub_document.delete(to_trash=False)


class RecentDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        if user.is_authenticated:
            new_recent, created = self.model.objects.get_or_create(
                user=user, document=document
            )
            if not created:
                # document already in the recent list, just save to force
                # accessed date and time update
                new_recent.save()

            recent_to_delete = self.filter(user=user).values_list('pk', flat=True)[setting_recent_access_count.value:]
            self.filter(pk__in=list(recent_to_delete)).delete()
        return new_recent

    def get_by_natural_key(self, datetime_accessed, document_natural_key, user_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        User = get_user_model()
        try:
            document = Document.objects.get_by_natural_key(*document_natural_key)
        except Document.DoesNotExist:
            raise self.model.DoesNotExist
        else:
            try:
                user = User.objects.get_by_natural_key(*user_natural_key)
            except User.DoesNotExist:
                raise self.model.DoesNotExist

        return self.get(
            document__pk=document.pk, user__pk=user.pk,
            datetime_accessed=datetime_accessed
        )

    def get_for_user(self, user):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        if user.is_authenticated:
            return Document.objects.filter(
                recent__user=user
            ).order_by('-recent__datetime_accessed')
        else:
            return Document.objects.none()


class TrashCanManager(models.Manager):
    def get_queryset(self):
        return super(
            TrashCanManager, self
        ).get_queryset().filter(in_trash=True)


class TrashCanQuerySet(models.QuerySet):
    def delete(self, to_trash=True):
        for instance in self:
            instance.delete(to_trash=to_trash)
