from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import BinaryDependency, PythonDependency

from .backends.python import pdfinfo_path, pdftoppm_path
from .classes import libreoffice_path

BinaryDependency(
    label='LibreOffice', module=__name__, name='libreoffice',
    path=libreoffice_path
)
BinaryDependency(
    label='PDF Info', help_text=_(
        'Utility from the poppler-utils package used to inspect PDF files.'
    ), module=__name__, name='pdfinfo', path=pdfinfo_path
)
BinaryDependency(
    label='PDF to PPM', help_text=_(
        'Utility from the popper-utils package used to extract pages '
        'from PDF files into PPM format images.'
    ), module=__name__, name='pdftoppm', path=pdftoppm_path
)
PythonDependency(
    copyright_attribute='PIL.__doc__', module=__name__, name='Pillow',
    version_string='==7.1.2',
)
PythonDependency(
    module=__name__, name='PyPDF2', version_string='==1.26.0'
)
