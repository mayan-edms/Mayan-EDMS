from __future__ import absolute_import

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .forms import RegistrationForm
from .models import RegistrationSingleton
from .tasks import task_registration_register


def form_view(request):
    registration = RegistrationSingleton.objects.get()

    if registration.registered:
        messages.error(request, _(u'Your copy is already registered.'))
        return HttpResponseRedirect(reverse('main:home'))

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            task_registration_register.apply_async(args=[form.cleaned_data], queue='tools')
            messages.success(request, _(u'Thank you for registering.'))
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = RegistrationForm()

    return render_to_response('main/generic_form.html', {
        'title': _(u'Registration form'),
        'form': form,
    }, context_instance=RequestContext(request))
