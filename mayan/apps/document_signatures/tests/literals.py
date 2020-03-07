from __future__ import unicode_literals

import os

from django.conf import settings

TEST_SIGNED_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'document_signatures', 'tests', 'contrib',
    'sample_documents', 'mayan_11_1.pdf.gpg'
)
TEST_SIGNATURE_FILE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'document_signatures', 'tests', 'contrib',
    'sample_documents', 'mayan_11_1.pdf.sig'
)
TEST_SIGNATURE_ID = 'XVkoGKw35yU1iq11dZPiv7uAY7k'
