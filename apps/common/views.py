from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect


def password_change_done(request):
    """
    View called when the new user password has been accepted
    """

    messages.success(request, _(u'Your password has been successfully changed.'))
    return redirect('home')


def multi_object_action_view(request):
    """
        Proxy view called first when usuing a multi object action, which
        then redirects to the appropiate specialized view
    """

    action = request.GET.get('action', None)
    id_list = u','.join([key[3:] for key in request.GET.keys() if key.startswith('pk_')])

    if not action:
        messages.error(request, _(u'No action selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if not id_list:
        messages.error(request, _(u'Must select at least one item.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect('%s?id_list=%s' % (action, id_list))
