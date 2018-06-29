# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import override_settings

from common.tests import BaseTestCase, GenericViewTestCase

from .mixins import DocumentTestMixin


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=False)
@override_settings(OCR_AUTO_OCR=False)
class GenericDocumentTestCase(DocumentTestMixin, BaseTestCase):
    """Base test case when testing models or classes"""


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=False)
@override_settings(OCR_AUTO_OCR=False)
class GenericDocumentViewTestCase(DocumentTestMixin, GenericViewTestCase):
    """Base test case when testing views"""
