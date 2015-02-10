from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .models import RegistrationSingleton


def is_not_registered(context):
    return RegistrationSingleton.registration_state() is False


form_view = {'text': _('Registration'), 'view': 'registration:form_view', 'famfam': 'telephone', 'condition': is_not_registered}
