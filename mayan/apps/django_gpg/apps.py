from __future__ import unicode_literals

from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_object, menu_setup, menu_sidebar
from common.utils import encapsulate
from navigation import SourceColumn

from .api import Key, KeyStub
from .links import (
    link_key_delete, link_key_query, link_key_receive, link_key_setup,
    link_public_keys
)


class DjangoGPGApp(MayanAppConfig):
    app_url = 'gpg'
    name = 'django_gpg'
    verbose_name = _('Django GPG')

    def ready(self):
        super(DjangoGPGApp, self).ready()

        SourceColumn(source=Key, label='ID', attribute='key_id')
        SourceColumn(
            source=Key, label='Owner', attribute=encapsulate(
                lambda key: ', '.join(key.uids)
            )
        )

        SourceColumn(
            source=KeyStub, label='ID', attribute=encapsulate(
                lambda key: '...{0}'.format(key.key_id[-16:])
            )
        )
        SourceColumn(source=KeyStub, label='Type', attribute='key_type')
        SourceColumn(
            source=KeyStub, label='Creation date', attribute=encapsulate(
                lambda key: datetime.fromtimestamp(int(key.date))
            )
        )
        SourceColumn(
            source=KeyStub, label='Expiration date', attribute=encapsulate(
                lambda key: datetime.fromtimestamp(int(key.expires)) if key.expires else _('No expiration')
            )
        )
        SourceColumn(source=KeyStub, label='Length', attribute='length')
        SourceColumn(
            source=KeyStub, label='Identities', attribute=encapsulate(
                lambda key: ', '.join(key.uids)
            )
        )

        menu_object.bind_links(links=(link_key_delete,), sources=(Key,))
        menu_object.bind_links(links=(link_key_receive,), sources=(KeyStub,))
        menu_setup.bind_links(links=(link_key_setup,))
        menu_sidebar.bind_links(
            links=(link_public_keys, link_key_query),
            sources=(
                'django_gpg:key_delete', 'django_gpg:key_public_list',
                'django_gpg:key_query', 'django_gpg:key_query_results',
            )
        )
