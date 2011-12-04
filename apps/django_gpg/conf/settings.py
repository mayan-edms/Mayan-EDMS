'''
Configuration options for the django_gpg app
'''

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'django_gpg',
    module=u'django_gpg.conf.settings',
    settings=[
        {'name': u'KEYSERVERS', 'global_name': u'SIGNATURES_KEYSERVERS', 'default': ['keyserver.ubuntu.com'], 'description': _(u'List of keyservers to be queried for unknown keys.')},
    ]
)
