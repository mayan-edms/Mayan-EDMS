from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login, password_change
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from stronghold.decorators import public

from .forms import EmailAuthenticationForm, UsernameAuthenticationForm
from .settings import setting_login_method, setting_maximum_session_length


@public
def login_view(request):
    """
    Control how the use is to be authenticated, options are 'email' and
    'username'
    """
    kwargs = {'template_name': 'appearance/login.html'}

    if setting_login_method.value == 'email':
        kwargs['authentication_form'] = EmailAuthenticationForm
    else:
        kwargs['authentication_form'] = UsernameAuthenticationForm

    if not request.user.is_authenticated():
        context = {'appearance_type': 'plain'}

        result = login(request, extra_context=context, **kwargs)
        if request.method == 'POST':
            form = kwargs['authentication_form'](request, data=request.POST)
            if form.is_valid():
                if form.cleaned_data['remember_me']:
                    request.session.set_expiry(
                        setting_maximum_session_length.value
                    )
                else:
                    request.session.set_expiry(0)
        return result
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
