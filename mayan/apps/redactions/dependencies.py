from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import (
    GoogleFontDependency, JavaScriptDependency
)

JavaScriptDependency(
    label=_('JavaScript image cropper'), module=__name__, name='cropperjs',
    version_string='=1.4.1'
)
JavaScriptDependency(
    module=__name__, name='jquery-cropper', version_string='=1.0.0'
)
