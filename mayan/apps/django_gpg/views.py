from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    ConfirmView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectDetailView, SingleObjectDownloadView, SingleObjectListView,
    SimpleView
)

from .forms import KeyDetailForm, KeySearchForm
from .icons import (
    icon_key_setup, icon_keyserver_search, icon_private_keys,
    icon_public_keys
)
from .links import link_key_query, link_key_upload
from .literals import KEY_TYPE_PUBLIC
from .models import Key
from .permissions import (
    permission_key_delete, permission_key_download, permission_key_receive,
    permission_key_upload, permission_key_view, permission_keyserver_query
)

logger = logging.getLogger(__name__)


class KeyDeleteView(SingleObjectDeleteView):
    model = Key
    object_permission = permission_key_delete

    def get_extra_context(self):
        return {'title': _('Delete key: %s') % self.get_object()}

    def get_post_action_redirect(self):
        if self.get_object().key_type == KEY_TYPE_PUBLIC:
            return reverse_lazy(viewname='django_gpg:key_public_list')
        else:
            return reverse_lazy(viewname='django_gpg:key_private_list')


class KeyDetailView(SingleObjectDetailView):
    form_class = KeyDetailForm
    model = Key
    object_permission = permission_key_view

    def get_extra_context(self):
        return {
            'title': _('Details for key: %s') % self.get_object(),
        }


class KeyDownloadView(SingleObjectDownloadView):
    model = Key
    object_permission = permission_key_download

    def get_download_file_object(self):
        return self.object.key_data

    def get_download_filename(self):
        return self.object.key_id


class KeyReceive(ConfirmView):
    post_action_redirect = reverse_lazy(viewname='django_gpg:key_public_list')
    view_permission = permission_key_receive

    def get_extra_context(self):
        return {
            'message': _('Import key ID: %s?') % self.kwargs['key_id'],
            'title': _('Import key'),
        }

    def view_action(self):
        try:
            Key.objects.receive_key(key_id=self.kwargs['key_id'])
        except Exception as exception:
            messages.error(
                message=_(
                    'Unable to import key: %(key_id)s; %(error)s'
                ) % {
                    'key_id': self.kwargs['key_id'],
                    'error': exception,
                }, request=self.request
            )
        else:
            messages.success(
                message=_('Successfully received key: %(key_id)s') % {
                    'key_id': self.kwargs['key_id'],
                }, request=self.request
            )


class KeyQueryResultView(SingleObjectListView):
    view_permission = permission_keyserver_query

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_key_setup,
            'no_results_main_link': link_key_query.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Use names, last names, key ids or emails to search '
                'public keys to import from the keyserver.'
            ),
            'no_results_title': _(
                'No results returned'
            ),
            'title': _('Key query results'),
        }

    def get_source_queryset(self):
        term = self.request.GET.get('term')
        if term:
            return Key.objects.search(query=term)
        else:
            return ()


class KeyQueryView(SimpleView):
    template_name = 'appearance/generic_form.html'
    view_permission = permission_keyserver_query

    def get_extra_context(self):
        return {
            'form': self.get_form(),
            'form_action': reverse(viewname='django_gpg:key_query_results'),
            'submit_icon_class': icon_keyserver_search,
            'submit_label': _('Search'),
            'submit_method': 'GET',
            'title': _('Query key server'),
        }

    def get_form(self):
        if ('term' in self.request.GET) and self.request.GET['term'].strip():
            term = self.request.GET['term']
            return KeySearchForm(initial={'term': term})
        else:
            return KeySearchForm()


class KeyUploadView(SingleObjectCreateView):
    fields = ('key_data',)
    model = Key
    post_action_redirect = reverse_lazy(viewname='django_gpg:key_public_list')
    view_permission = permission_key_upload

    def get_extra_context(self):
        return {
            'title': _('Upload new key'),
        }


class PrivateKeyListView(SingleObjectListView):
    object_permission = permission_key_view
    source_queryset = Key.objects.private_keys()

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_private_keys,
            'no_results_main_link': link_key_upload.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Private keys are used to signed documents. '
                'Private keys can only be uploaded by the user.'
                'The view to upload private and public keys is the same.'
            ),
            'no_results_title': _(
                'There no private keys'
            ),
            'title': _('Private keys')
        }


class PublicKeyListView(SingleObjectListView):
    object_permission = permission_key_view
    source_queryset = Key.objects.public_keys()

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_public_keys,
            'no_results_main_link': link_key_upload.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Public keys are used to verify signed documents. '
                'Public keys can be uploaded by the user or downloaded '
                'from keyservers. The view to upload private and public '
                'keys is the same.'
            ),
            'no_results_title': _(
                'There no public keys'
            ),
            'title': _('Public keys')
        }
