from __future__ import unicode_literals

TEST_DOCUMENT_CONTENT = 'Sample text'
TEST_PARSING_INDEX_NODE_TEMPLATE = '{% if "sample" in document.latest_version.content|join:" "|lower %}sample{% endif %}'
