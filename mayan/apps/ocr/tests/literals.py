from __future__ import unicode_literals

TEST_OCR_INDEX_NODE_TEMPLATE = '{% if "mayan" in document.latest_version.ocr_content|join:" "|lower %}mayan{% endif %}'
TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL = 'mayan'
