from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.generics import SimpleView, SingleObjectListView
from permissions import Permission

from .api import Key
from .forms import KeySearchForm
from .permissions import (
    permission_key_delete, permission_key_receive, permission_key_view,
    permission_keyserver_query
)
from .runtime import gpg

logger = logging.getLogger(__name__)


def key_receive(request, key_id):
    Permission.check_permissions(request.user, (permission_key_receive,))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            gpg.receive_key(key_id=key_id)
        except Exception as exception:
            messages.error(
                request,
                _('Unable to import key: %(key_id)s; %(error)s') %
                {
                    'key_id': key_id,
                    'error': exception,
                }
            )
            return HttpResponseRedirect(previous)
        else:
            messages.success(
                request,
                _('Successfully received key: %(key_id)s') %
                {
                    'key_id': key_id,
                }
            )

            return redirect('django_gpg:key_public_list')

    return render_to_response('appearance/generic_confirm.html', {
        'message': _('Import key ID: %s?') % key_id,
        'previous': previous,
        'title': _('Import key'),
    }, context_instance=RequestContext(request))


class PublicKeyListView(SingleObjectListView):
    view_permission = permission_key_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'title': self.get_title()
        }

    def get_queryset(self):
        return Key.get_all(gpg)

    def get_title(self):
        return _('Public keys')


class PrivateKeyListView(PublicKeyListView):
    def get_title(self):
        return _('Private keys')

    def get_queryset(self):
        return Key.get_all(gpg, secret=True)


def key_delete(request, fingerprint, key_type):
    Permission.check_permissions(request.user, (permission_key_delete,))

    secret = key_type == 'sec'
    key = Key.get(gpg, fingerprint, secret=secret)

    post_action_redirect = redirect('django_gpg:key_public_list')
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            gpg.delete_key(key)
            messages.success(request, _('Key: %s, deleted successfully.') % fingerprint)
            return HttpResponseRedirect(next)
        except Exception as exception:
            messages.error(request, exception)
            return HttpResponseRedirect(previous)

    return render_to_response('appearance/generic_confirm.html', {
        'title': _('Delete key'),
        'delete_view': True,
        'message': _(
            'Delete key %s? If you delete a public key that is part of a '
            'public/private pair the private key will be deleted as well.'
        ) % key,
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


class KeyQueryView(SimpleView):
    template_name = 'appearance/generic_form.html'
    view_permission = permission_keyserver_query

    def get_form(self):
        if ('term' in self.request.GET) and self.request.GET['term'].strip():
            term = self.request.GET['term']
            return KeySearchForm(initial={'term': term})
        else:
            return KeySearchForm()

    def get_extra_context(self):
        return {
            'form': self.get_form(),
            'form_action': reverse('django_gpg:key_query_results'),
            'submit_icon': 'fa fa-search',
            'submit_label': _('Search'),
            'submit_method': 'GET',
            'title': _('Query key server'),
        }


class KeyQueryResultView(SingleObjectListView):
    view_permission = permission_keyserver_query

    def get_extra_context(self):
        return {
            'hide_object': True,
            'title': _('Key query results'),
        }

    def get_queryset(self):
        term = self.request.GET.get('term')
        if term:
            return gpg.query(term)
        else:
            return ()
