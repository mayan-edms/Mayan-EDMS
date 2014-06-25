"""Configuration options for the linking app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'linking',
    module=u'linking.conf.settings',
    settings=[
        {'name': u'SHOW_EMPTY_SMART_LINKS', 'global_name': u'LINKING_SHOW_EMPTY_SMART_LINKS', 'default': True, 'description': _(u'Show smart link that don\'t return any documents.')},
    ]
)
