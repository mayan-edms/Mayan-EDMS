# -*- coding: utf-8 -*-

from __future__ import unicode_literals

TEST_DOCUMENT_CONTENT = 'Mayan EDMS Documentation'
TEST_DOCUMENT_CONTENT_DEU_1 = 'Repository für elektronische Dokumente.'
TEST_DOCUMENT_CONTENT_DEU_2 = 'Es bietet einen'

TEST_OCR_INDEX_NODE_TEMPLATE = '{% if "mayan" in document.latest_version.ocr_content|join:" "|lower %}mayan{% endif %}'
TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL = 'mayan'
