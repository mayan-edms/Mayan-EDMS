from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_file_models import DocumentFile
from mayan.apps.documents.models.document_version_models import DocumentVersion

DEFAULT_DOCUMENT_BODY_TEMPLATE = _(
    'Attached to this email is the {{ object_name }}: {{ object }}\n\n '
    '--------\n '
    'This email has been sent from %(project_title)s (%(project_website)s)'
)
DEFAULT_DOCUMENT_SUBJECT_TEMPLATE = _('{{ object_name }}: {{ object }}')
DEFAULT_LINK_BODY_TEMPLATE = _(
    'To access this {{ object_name }} click on the following link: '
    '{{ link }}\n\n--------\n '
    'This email has been sent from %(project_title)s (%(project_website)s)'
)
DEFAULT_LINK_SUBJECT_TEMPLATE = _('Link for {{ object_name }}: {{ object }}')
EMAIL_SEPARATORS = (',', ';')

DOCUMENT_FILE_CONTENT_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_file_content'
DOCUMENT_FILE_MIME_TYPE_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_file_mime_type'

DOCUMENT_VERSION_CONTENT_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_version_content'
DOCUMENT_VERSION_MIME_TYPE_FUNCTION_DOTTED_PATH = 'mayan.apps.mailer.utils.get_document_version_mime_type'

MODEL_SEND_FUNCTION_DOTTED_PATH = {
    DocumentFile: {
        'content_function_dotted_path': DOCUMENT_FILE_CONTENT_FUNCTION_DOTTED_PATH,
        'mime_type_function_dotted_path': DOCUMENT_FILE_MIME_TYPE_FUNCTION_DOTTED_PATH
    },
    DocumentVersion: {
        'content_function_dotted_path': DOCUMENT_VERSION_CONTENT_FUNCTION_DOTTED_PATH,
        'mime_type_function_dotted_path': DOCUMENT_VERSION_MIME_TYPE_FUNCTION_DOTTED_PATH
    }
}
