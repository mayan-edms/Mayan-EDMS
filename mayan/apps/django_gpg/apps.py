from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from hkp import Key as KeyServerKey

from common import menu_object, menu_setup, menu_sidebar

from .api import Key
from .links import (
    link_key_delete, link_key_query, link_key_receive, link_key_setup,
    link_public_keys
)


class DjangoGPGApp(apps.AppConfig):
    name = 'django_gpg'
    verbose_name = _('Django GPG')

    def ready(self):
        menu_object.bind_links(links=[link_key_delete], sources=[Key])
        menu_object.bind_links(links=[link_key_receive], sources=[KeyServerKey])
        menu_setup.bind_links(links=[link_key_setup])
        menu_sidebar.bind_links(links=[link_public_keys, link_key_query], sources=['django_gpg:key_delete', 'django_gpg:key_public_list', 'django_gpg:key_query'])
