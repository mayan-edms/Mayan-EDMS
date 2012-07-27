from __future__ import absolute_import

import logging

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from permissions.models import Permission
from common.utils import encapsulate

from .api import Key
from .runtime import gpg
from .exceptions import KeyImportError
from .forms import KeySearchForm
from .permissions import (PERMISSION_KEY_VIEW, PERMISSION_KEY_DELETE,
    PERMISSION_KEYSERVER_QUERY, PERMISSION_KEY_RECEIVE)

logger = logging.getLogger(__name__)


def key_receive(request, key_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_KEY_RECEIVE])

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            term = request.GET.get('term')
            results = gpg.query(term)
            keys_dict = dict([(key.keyid, key) for key in results])
            key = gpg.import_key(keys_dict[key_id].key)
            messages.success(request, _(u'Key: %s, imported successfully.') % key)
            return HttpResponseRedirect(next)
        except (KeyImportError, KeyError, TypeError), e:
            messages.error(
                request,
                _(u'Unable to import key id: %(key_id)s; %(error)s') %
                {
                    'key_id': key_id,
                    'error': e,
                }
            )
            return HttpResponseRedirect(previous)

    return render_to_response('generic_confirm.html', {
        'title': _(u'Import key'),
        'message': _(u'Are you sure you wish to import key id: %s?') % key_id,
        'form_icon': 'key_add.png',
        'next': next,
        'previous': previous,
        'submit_method': 'GET',

    }, context_instance=RequestContext(request))


def key_list(request, secret=True):
    Permission.objects.check_permissions(request.user, [PERMISSION_KEY_VIEW])

    if secret:
        object_list = Key.get_all(gpg, secret=True)
        title = _(u'private keys')
    else:
        object_list = Key.get_all(gpg)
        title = _(u'public keys')

    return render_to_response('generic_list.html', {
        'object_list': object_list,
        'title': title,
        'hide_object': True,
        'extra_columns': [
            {
                'name': _(u'Key ID'),
                'attribute': 'key_id',
            },
            {
                'name': _(u'Owner'),
                'attribute': encapsulate(lambda x: u', '.join(x.uids)),
            },
        ]
    }, context_instance=RequestContext(request))


def key_delete(request, fingerprint, key_type):
    Permission.objects.check_permissions(request.user, [PERMISSION_KEY_DELETE])

    secret = key_type == 'sec'
    key = Key.get(gpg, fingerprint, secret=secret)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            gpg.delete_key(key)
            messages.success(request, _(u'Key: %s, deleted successfully.') % fingerprint)
            return HttpResponseRedirect(next)
        except Exception, msg:
            messages.error(request, msg)
            return HttpResponseRedirect(previous)

    return render_to_response('generic_confirm.html', {
        'title': _(u'Delete key'),
        'delete_view': True,
        'message': _(u'Are you sure you wish to delete key: %s?  If you try to delete a public key that is part of a public/private pair the private key will be deleted as well.') % key,
        'form_icon': 'key_delete.png',
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


def key_query(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_KEYSERVER_QUERY])

    subtemplates_list = []
    term = request.GET.get('term')

    form = KeySearchForm(initial={'term': term})
    subtemplates_list.append(
        {
            'name': 'generic_form_subtemplate.html',
            'context': {
                'title': _(u'Query key server'),
                'form': form,
                'submit_method': 'GET',
            },
        }
    )

    if term:
        results = gpg.query(term)
        subtemplates_list.append(
            {
                'name': 'generic_list_subtemplate.html',
                'context': {
                    'title': _(u'results'),
                    'object_list': results,
                    'hide_object': True,
                    'extra_columns': [
                        {
                            'name': _(u'ID'),
                            'attribute': 'keyid',
                        },
                        {
                            'name': _(u'type'),
                            'attribute': 'algo',
                        },
                        {
                            'name': _(u'creation date'),
                            'attribute': 'creation_date',
                        },
                        {
                            'name': _(u'disabled'),
                            'attribute': 'disabled',
                        },
                        {
                            'name': _(u'expiration date'),
                            'attribute': 'expiration_date',
                        },
                        {
                            'name': _(u'expired'),
                            'attribute': 'expired',
                        },
                        {
                            'name': _(u'length'),
                            'attribute': 'key_length',
                        },
                        {
                            'name': _(u'revoked'),
                            'attribute': 'revoked',
                        },

                        {
                            'name': _(u'Identifies'),
                            'attribute': encapsulate(lambda x: u', '.join([identity.uid for identity in x.identities])),
                        },
                    ]
                },
            }
        )

    return render_to_response('generic_form.html', {
        'subtemplates_list': subtemplates_list,
    }, context_instance=RequestContext(request))
