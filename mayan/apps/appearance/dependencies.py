from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import (
    GoogleFontDependency, JavaScriptDependency
)

GoogleFontDependency(
    label=_('Lato font'), module=__name__, name='lato',
    url='https://fonts.googleapis.com/css?family=Lato:400,700,400italic'
)
JavaScriptDependency(
    label=_('Bootstrap'), module=__name__, name='bootstrap',
    version_string='=3.4.1'
)
JavaScriptDependency(
    label=_('Bootswatch'), module=__name__, name='bootswatch',
    replace_list=[
        {
            'filename_pattern': 'bootstrap.*.css',
            'content_patterns': [
                {
                    'search': '"https://fonts.googleapis.com/css?family=Lato:400,700,400italic"',
                    'replace': '../../../google_fonts/lato/import.css',
                }
            ]
        }
    ], version_string='=3.4.1'
)
JavaScriptDependency(
    label=_('Fancybox'), module=__name__, name='@fancyapps/fancybox',
    version_string='=3.2.5'
)
JavaScriptDependency(
    label=_('FontAwesome'), module=__name__,
    name='@fortawesome/fontawesome-free', version_string='=5.6.3'
)
JavaScriptDependency(
    label=_('jQuery'), module=__name__, name='jquery', version_string='=3.4.1'
)
JavaScriptDependency(
    label=_('JQuery Form'), module=__name__, name='jquery-form',
    version_string='=4.2.2'
)
JavaScriptDependency(
    label=_('jQuery Lazy Load'), module=__name__, name='jquery-lazyload',
    version_string='=1.9.3'
)
JavaScriptDependency(
    label=_('JQuery Match Height'), module=__name__, name='jquery-match-height',
    version_string='=0.7.2'
)
JavaScriptDependency(
    label=_('Select 2'), module=__name__, name='select2',
    version_string='=4.0.3'
)
JavaScriptDependency(
    label=_('Toastr'), module=__name__, name='toastr', version_string='=2.1.4'
)
JavaScriptDependency(
    label=_('URI.js'), module=__name__, name='urijs', version_string='=1.19.1'
)
