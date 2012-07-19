from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from .api import bootstrap_options


def bootstrap_type_list(request):
    # TODO: Check for superadmin
    
    context = {
        'object_list': bootstrap_options.values(),
        'title': _(u'database bootstrap setups'),
        'hide_link': True,
        'extra_columns': [
            {'name': _(u'description'), 'attribute': 'description'},
            #{'name': _(u'label'), 'attribute': encapsulate(lambda document: document.checkout_info().expiration_datetime)},
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def bootstrap_execute(request, bootstrap_name):
    bootstrap = bootstrap_options[bootstrap_name]
    
    post_action_redirect = reverse('bootstrap_type_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            bootstrap.execute()
        except Exception, exc:
            messages.error(request, _(u'Error executing bootstrap setup; %s') % exc)
        else:
            messages.success(request, _(u'Bootstrap setup "%s" executed successfully.') % bootstrap)
            return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'bootstrap setup'),
        'delete_view': False,
        'previous': previous,
        'next': next,
        #'form_icon': u'basket_remove.png',
        'object': bootstrap,
    }

    context['title'] = _(u'Are you sure you wish to execute the database bootstrap named: %s?') % bootstrap.label

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
