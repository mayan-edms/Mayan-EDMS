from django.apps import apps
from django.db.models import F, Max
from django.utils.translation import ugettext_lazy as _

from .classes import DuplicateBackend


class DuplicateBackendFileChecksum(DuplicateBackend):
    label = _('Exact document file checksum')

    @classmethod
    def verify(cls, document):
        return document.file_latest

    def process(self, document):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        # Get the documents whose latest file matches the checksum
        # of the current document and exclude the current document

        return Document.objects.annotate(
            max_timestamp=Max('files__timestamp')
        ).filter(
            files__timestamp=F('max_timestamp'),
            files__checksum=document.file_latest.checksum
        ).exclude(pk=document.pk)


class DuplicateBackendLabel(DuplicateBackend):
    label = _('Exact document label')

    def process(self, document):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        return Document.objects.filter(
            label=document.label
        ).exclude(pk=document.pk)
