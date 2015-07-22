from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login, password_change
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from .forms import EmailAuthenticationForm
from .settings import setting_login_method


def login_view(request):
    """
    Control how the use is to be authenticated, options are 'email' and
    'username'
    """
    kwargs = {'template_name': 'appearance/login.html'}

    if setting_login_method.value == 'email':
        kwargs['authentication_form'] = EmailAuthenticationForm

    if not request.user.is_authenticated():
        context = {'appearance_type': 'plain'}
        return login(request, extra_context=context, **kwargs)
    else:
        return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))


def password_change_view(request):
    """
    Password change wrapper for better control
    """
    context = {'title': _('Current user password change')}

    return password_change(
        request,
        extra_context=context,
        template_name='appearance/generic_form.html',
        post_change_redirect=reverse('authentication:password_change_done'),
    )


def password_change_done(request):
    """
    View called when the new user password has been accepted
    """

    messages.success(
        request, _('Your password has been successfully changed.')
    )
    return redirect('common:current_user_details')
