from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import (
    BinaryDependency, JavaScriptDependency, PythonDependency
)

from .literals import DEFAULT_BINARY_SCANIMAGE_PATH
from .settings import setting_backend_arguments

BinaryDependency(
    label='SANE scanimage', help_text=_(
        'Utility provided by the SANE package. Used to control the scanner '
        'and obtained the scanned document image.'
    ), module=__name__, name='scanimage', path=setting_backend_arguments.value.get(
        'mayan.apps.sources.source_backends.SourceBackendSANEScanner', {}
    ).get('scanimage_path', DEFAULT_BINARY_SCANIMAGE_PATH)
)
JavaScriptDependency(
    module=__name__, name='dropzone', version_string='=5.9.2'
)
PythonDependency(
    module=__name__, name='flanker', version_string='==0.9.11'
)
