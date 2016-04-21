from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.links import link_acl_list
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_object, menu_setup, menu_sidebar
)
from common.classes import Package
from navigation import SourceColumn

from .classes import KeyStub
from .links import (
    link_key_delete, link_key_detail, link_key_download, link_key_query,
    link_key_receive, link_key_setup, link_key_upload, link_private_keys,
    link_public_keys
)
from .permissions import (
    permission_key_delete, permission_key_download, permission_key_sign,
    permission_key_view
)


class DjangoGPGApp(MayanAppConfig):
    app_url = 'gpg'
    name = 'django_gpg'
    test = True
    verbose_name = _('Django GPG')

    def ready(self):
        super(DjangoGPGApp, self).ready()

        Key = self.get_model('Key')

        ModelPermission.register(
            model=Key, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_key_delete, permission_key_download,
                permission_key_sign, permission_key_view
            )
        )

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

        SourceColumn(source=Key, label=_('Key ID'), attribute='key_id')
        SourceColumn(source=Key, label=_('User ID'), attribute='user_id')

        SourceColumn(source=KeyStub, label=_('Key ID'), attribute='key_id')
        SourceColumn(source=KeyStub, label=_('Type'), attribute='key_type')
        SourceColumn(
            source=KeyStub, label=_('Creation date'), attribute='date'
        )
        SourceColumn(
            source=KeyStub, label=_('Expiration date'),
            func=lambda context: context['object'].expires or _('No expiration')
        )
        SourceColumn(source=KeyStub, label=_('Length'), attribute='length')
        SourceColumn(
            source=KeyStub, label=_('User ID'),
            func=lambda context: ', '.join(context['object'].user_id)
        )

        menu_object.bind_links(links=(link_key_detail,), sources=(Key,))
        menu_object.bind_links(links=(link_key_receive,), sources=(KeyStub,))

        menu_object.bind_links(
            links=(link_acl_list, link_key_delete, link_key_download,),
            sources=(Key,)
        )
        menu_setup.bind_links(links=(link_key_setup,))
        menu_facet.bind_links(
            links=(link_private_keys, link_public_keys),
            sources=(
                'django_gpg:key_public_list', 'django_gpg:key_private_list',
                'django_gpg:key_query', 'django_gpg:key_query_results', Key,
                KeyStub
            )
        )
        menu_sidebar.bind_links(
            links=(link_key_query, link_key_upload),
            sources=(
                'django_gpg:key_public_list', 'django_gpg:key_private_list',
                'django_gpg:key_query', 'django_gpg:key_query_results', Key,
                KeyStub
            )
        )
