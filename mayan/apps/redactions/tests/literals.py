import os

from django.conf import settings

TEST_REDACTION_ARGUMENT = "{'left': 10, 'top': 10, 'right': 10, 'bottom': 10}"
TEST_REDACTION_ARGUMENT_EDITED = "{'left': 20, 'top': 20, 'right': 20, 'bottom': 20}"

TEST_REDACTION_DOCUMENT_FILENAME = 'black_upper_left_corner.png'
TEST_REDACTION_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'redactions', 'tests', 'contrib',
    'sample_documents', TEST_REDACTION_DOCUMENT_FILENAME
)
