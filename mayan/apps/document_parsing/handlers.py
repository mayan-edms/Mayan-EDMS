from __future__ import unicode_literals

import logging

from django.apps import apps

from .settings import setting_auto_ocr
from .parsers import Parser

logger = logging.getLogger(__name__)


def handler_parse_document_version(sender, instance, **kwargs):
    if kwargs['created']:
        Parser.parse_document_version(document_version=instance)
