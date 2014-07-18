from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .models import RegistrationSingleton


def is_not_registered(context):
    return RegistrationSingleton.registration_state() is False


form_view = {'text': _('Registration'), 'view': 'form_view', 'famfam': 'telephone', 'condition': is_not_registered}
