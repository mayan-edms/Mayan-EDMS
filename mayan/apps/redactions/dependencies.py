from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import JavaScriptDependency

JavaScriptDependency(
    label=_('JavaScript image cropper'), module=__name__, name='cropperjs',
    version_string='=1.5.2'
)
JavaScriptDependency(
    module=__name__, name='jquery-cropper', version_string='=1.0.1'
)
