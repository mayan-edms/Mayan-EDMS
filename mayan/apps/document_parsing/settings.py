from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

namespace = Namespace(label=_('Document parsing'), name='document_parsing')

setting_auto_parsing = namespace.add_setting(
    global_name='DOCUMENT_PARSING_AUTO_PARSING', default=True,
    help_text=_(
        'Set new document types to perform parsing automatically by default.'
    )
)
setting_pdftotext_path = namespace.add_setting(
    global_name='DOCUMENT_PARSING_PDFTOTEXT_PATH',
    default='/usr/bin/pdftotext',
    help_text=_(
        'File path to poppler\'s pdftotext program used to extract text '
        'from PDF files.'
    ),
    is_path=True
)
