from __future__ import unicode_literals

import logging
import sys
import traceback

from django.apps import apps
from django.conf import settings
from django.db import models, transaction

from .events import (
    event_parsing_document_content_deleted,
    event_parsing_document_version_finish
)
from .parsers import Parser
from .signals import post_document_version_parsing

logger = logging.getLogger(__name__)


class DocumentVersionPageContentManager(models.Manager):
    def delete_content_for(self, document, user=None):
        with transaction.atomic():
            for document_page in document.pages.all():
                self.filter(
                    document_version_page=document_page.content_object
                ).delete()

            event_parsing_document_content_deleted.commit(
                actor=user, target=document
            )

    def process_document_version(self, document_version):
        logger.info(
            'Starting parsing for document version: %s', document_version
        )
        logger.debug('document version: %d', document_version.pk)

        try:
            Parser.parse_document_version(document_version=document_version)
        except Exception as exception:
            logger.error(
                'Parsing error for document version: %d; %s',
                document_version.pk, exception,
            )

            if settings.DEBUG:
                result = []
                type, value, tb = sys.exc_info()
                result.append('%s: %s' % (type.__name__, value))
                result.extend(traceback.format_tb(tb))
                document_version.parsing_errors.create(
                    result='\n'.join(result)
                )
            else:
                document_version.parsing_errors.create(result=exception)
        else:
            logger.info(
                'Parsing complete for document version: %s', document_version
            )
            document_version.parsing_errors.all().delete()

            event_parsing_document_version_finish.commit(
                action_object=document_version.document,
                target=document_version
            )

            post_document_version_parsing.send(
                sender=document_version.__class__, instance=document_version
            )


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
