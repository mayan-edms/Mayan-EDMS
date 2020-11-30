from datetime import timedelta
import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Max
from django.utils.encoding import force_text
from django.utils.timezone import now

from mayan.apps.common.classes import ModelQueryFields


logger = logging.getLogger(name=__name__)


class DuplicatedDocumentManager(models.Manager):
    def clean_empty_duplicate_lists(self):
        self.filter(documents=None).delete()

    def get_duplicated_documents(self):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        return Document.valid.filter(
            pk__in=self.filter(documents__in_trash=False).values(
                'document_id'
            )
        )

    def get_duplicates_of(self, document):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        try:
            queryset = self.get(
                document=document
            ).documents.all()

            return Document.valid.filter(
                pk__in=queryset
            )
        except self.model.DoesNotExist:
            return Document.objects.none()

    def scan(self):
        """
        Find duplicates by iterating over all documents and then
        find matching latest files checksums
        """
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        for document in Document.valid.all():
            self.scan_for(document=document, scan_children=False)

    def scan_for(self, document, scan_children=True):
        """
        Find duplicates by matching latest file checksums
        """
        if not document.file_latest:
            return None

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        # Get the documents whose latest file matches the checksum
        # of the current document and exclude the current document

        duplicates = Document.objects.annotate(
            max_timestamp=Max('files__timestamp')
        ).filter(
            files__timestamp=F('max_timestamp'),
            files__checksum=document.file_latest.checksum
        ).exclude(pk=document.pk)

        if duplicates.exists():
            instance, created = self.get_or_create(document=document)
            instance.documents.add(*duplicates)
        else:
            self.filter(document=document).delete()

        if scan_children:
            for document in duplicates:
                self.scan_for(document=document, scan_children=False)
