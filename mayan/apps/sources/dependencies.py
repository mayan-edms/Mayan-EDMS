from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import (
    BinaryDependency, JavaScriptDependency, PythonDependency
)

from .settings import setting_scanimage_path

BinaryDependency(
    label='SANE scanimage', help_text=_(
        'Utility provided by the SANE package. Used to control the scanner '
        'and obtained the scanned document image.'
    ), module=__name__, name='scanimage', path=setting_scanimage_path.value
)
JavaScriptDependency(
    module=__name__, name='dropzone', version_string='=5.4.0'
)
PythonDependency(
    module=__name__, name='flanker', version_string='==0.9.0'
)
