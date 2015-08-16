from __future__ import unicode_literals

from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_object, menu_setup, menu_sidebar
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

        SourceColumn(source=Key, label=_('ID'), attribute='key_id')
        SourceColumn(
            source=Key, label=_('Owner'),
            func=lambda context: ', '.join(context['object'].uids)
        )

        SourceColumn(
            source=KeyStub, label=_('ID'),
            func=lambda context: '...{0}'.format(context['object'].key_id[-16:])
        )
        SourceColumn(source=KeyStub, label=_('Type'), attribute='key_type')
        SourceColumn(
            source=KeyStub, label=_('Creation date'),
            func=lambda context: datetime.fromtimestamp(
                int(context['object'].date)
            )
        )
        SourceColumn(
            source=KeyStub, label=_('Expiration date'),
            func=lambda context: datetime.fromtimestamp(int(context['object'].expires)) if context['object'].expires else _('No expiration')
        )
        SourceColumn(source=KeyStub, label=_('Length'), attribute='length')
        SourceColumn(
            source=KeyStub, label=_('Identities'),
            func=lambda context: ', '.join(context['object'].uids)
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
