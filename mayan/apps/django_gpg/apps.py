from __future__ import unicode_literals

from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_object, menu_setup, menu_sidebar
from common.classes import Package
from navigation import SourceColumn

from .api import Key, KeyStub
from .links import (
    link_key_delete, link_key_query, link_key_receive, link_key_setup,
    link_public_keys
)


class DjangoGPGApp(MayanAppConfig):
    app_url = 'gpg'
    name = 'django_gpg'
    test = True
    verbose_name = _('Django GPG')

    def ready(self):
        super(DjangoGPGApp, self).ready()

        Package(label='python-gnupg', license_text='''
Copyright (c) 2008-2014 by Vinay Sajip.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * The name(s) of the copyright holder(s) may not be used to endorse or
      promote products derived from this software without specific prior
      written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER(S) "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE COPYRIGHT HOLDER(S) BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        ''')

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
