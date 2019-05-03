from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import BinaryDependency

from .settings import setting_pdftotext_path

BinaryDependency(
    help_text=_(
        'Utility from the poppler-utils package used to text content '
        'from PDF files.'
    ), label='PDF to text', module=__name__, name='pdftotext',
    path=setting_pdftotext_path.value
)
