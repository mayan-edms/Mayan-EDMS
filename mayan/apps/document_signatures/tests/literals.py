import os

from django.conf import settings

DOCUMENT_SIGNATURE_DETACHED_ACTION_CLASS_PATH = 'mayan.apps.document_signatures.workflow_actions.DocumentSignatureDetachedAction'
DOCUMENT_SIGNATURE_EMBEDDED_ACTION_CLASS_PATH = 'mayan.apps.document_signatures.workflow_actions.DocumentSignatureEmbeddedAction'
TEST_SIGNED_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'document_signatures', 'tests', 'contrib',
    'sample_documents', 'mayan_11_1.pdf.gpg'
)
TEST_SIGNATURE_FILE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'document_signatures', 'tests', 'contrib',
    'sample_documents', 'mayan_11_1.pdf.sig'
)
TEST_SIGNATURE_ID = 'XVkoGKw35yU1iq11dZPiv7uAY7k'

TEST_SIGNED_DOCUMENT_COUNT = 2
TEST_UNSIGNED_DOCUMENT_COUNT = 4
