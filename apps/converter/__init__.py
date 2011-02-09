import tempfile

from documents.conf import settings as documents_settings

TEMPORARY_DIRECTORY = documents_settings.TEMPORARY_DIRECTORY if documents_settings.TEMPORARY_DIRECTORY else tempfile.mkdtemp()
