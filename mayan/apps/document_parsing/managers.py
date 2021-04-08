import logging
import sys
import traceback

from django.apps import apps
from django.conf import settings
from django.db import models, transaction

from .events import (
    event_parsing_document_file_content_deleted,
    event_parsing_document_file_finish
)
from .parsers import Parser
from .signals import signal_post_document_file_parsing

logger = logging.getLogger(name=__name__)


class DocumentFilePageContentManager(models.Manager):
    def delete_content_for(self, document_file, user=None):
        with transaction.atomic():
            for document_file_page in document_file.pages.all():
                self.filter(document_file_page=document_file_page).delete()

            event_parsing_document_file_content_deleted.commit(
                actor=user, action_object=document_file.document,
                target=document_file
            )

    def process_document_file(self, document_file):
        logger.info(
            'Starting parsing for document file: %s', document_file
        )
        logger.debug('document file: %d', document_file.pk)
        try:
            Parser.parse_document_file(document_file=document_file)

            logger.info(
                'Parsing complete for document file: %s', document_file
            )
            document_file.parsing_errors.all().delete()

            signal_post_document_file_parsing.send(
                sender=document_file.__class__,
                instance=document_file
            )

            event_parsing_document_file_finish.commit(
                action_object=document_file.document,
                target=document_file
            )
        except Exception as exception:
            logger.error(
                'Parsing error for document file: %d; %s',
                document_file.pk, exception, exc_info=True
            )

            if settings.DEBUG:
                result = []
                type, value, tb = sys.exc_info()
                result.append('%s: %s' % (type.__name__, value))
                result.extend(traceback.format_tb(tb))
                document_file.parsing_errors.create(
                    result='\n'.join(result)
                )
            else:
                document_file.parsing_errors.create(result=exception)


class DocumentTypeSettingsManager(models.Manager):
    def get_by_natural_key(self, document_type_natural_key):
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        try:
            document_type = DocumentType.objects.get_by_natural_key(document_type_natural_key)
        except DocumentType.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document_type__pk=document_type.pk)
