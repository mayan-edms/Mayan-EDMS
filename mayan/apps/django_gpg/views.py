from __future__ import absolute_import, unicode_literals

from datetime import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.utils import encapsulate
from permissions.models import Permission

from .api import Key
from .forms import KeySearchForm
from .permissions import (
    PERMISSION_KEY_DELETE, PERMISSION_KEY_RECEIVE, PERMISSION_KEY_VIEW,
    PERMISSION_KEYSERVER_QUERY
)
from .runtime import gpg

logger = logging.getLogger(__name__)


def key_receive(request, key_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_KEY_RECEIVE])

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
        'title': _('Import key'),
        'message': _('Are you sure you wish to import key id: %s?') % key_id,
        'previous': previous,
        'submit_method': 'GET',

    }, context_instance=RequestContext(request))


def key_list(request, secret=True):
    Permission.objects.check_permissions(request.user, [PERMISSION_KEY_VIEW])

    if secret:
        object_list = Key.get_all(gpg, secret=True)
        title = _('Private keys')
    else:
        object_list = Key.get_all(gpg)
        title = _('Public keys')

    return render_to_response('appearance/generic_list.html', {
        'object_list': object_list,
        'title': title,
        'hide_object': True,
        'extra_columns': [
            {
                'name': _('Key ID'),
                'attribute': 'key_id',
            },
            {
                'name': _('Owner'),
                'attribute': encapsulate(lambda x: ', '.join(x.uids)),
            },
        ]
    }, context_instance=RequestContext(request))


def key_delete(request, fingerprint, key_type):
    Permission.objects.check_permissions(request.user, [PERMISSION_KEY_DELETE])

    secret = key_type == 'sec'
    key = Key.get(gpg, fingerprint, secret=secret)

    post_action_redirect = None
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
        'message': _('Are you sure you wish to delete key: %s?  If you try to delete a public key that is part of a public/private pair the private key will be deleted as well.') % key,
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
            'name': 'appearance/generic_form_subtemplate.html',
            'context': {
                'title': _('Query key server'),
                'form': form,
                'submit_method': 'GET',
            },
        }
    )

    if term:
        results = gpg.query(term)
        subtemplates_list.append(
            {
                'name': 'appearance/generic_list_subtemplate.html',
                'context': {
                    'title': _('results'),
                    'object_list': results,
                    'hide_object': True,
                    'extra_columns': [
                        {
                            'name': _('ID'),
                            'attribute': encapsulate(lambda item: '...{0}'.format(item.key_id[-16:])),
                        },
                        {
                            'name': _('Type'),
                            'attribute': 'key_type',
                        },
                        {
                            'name': _('Creation date'),
                            'attribute': encapsulate(lambda x: datetime.fromtimestamp(int(x.date)))
                        },
                        {
                            'name': _('Expiration date'),
                            'attribute': encapsulate(lambda x: datetime.fromtimestamp(int(x.expires)) if x.expires else _('No expiration'))
                        },
                        {
                            'name': _('Length'),
                            'attribute': 'length',
                        },
                        {
                            'name': _('Identities'),
                            'attribute': encapsulate(lambda x: ', '.join(x.uids)),
                        },
                    ]
                },
            }
        )

    return render_to_response('appearance/generic_form.html', {
        'subtemplates_list': subtemplates_list,
    }, context_instance=RequestContext(request))
