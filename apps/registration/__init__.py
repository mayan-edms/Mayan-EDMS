from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError
from navigation.api import register_links
from common import about_view, license_view

from .models import RegistrationSingleton


def is_not_registered(context):
    return RegistrationSingleton.registration_state() == False
    

form_view = {'text': _('Registration'), 'view': 'form_view', 'famfam': 'telephone', 'condition': is_not_registered}

register_links(['form_view'], [about_view, license_view], menu_name='secondary_menu')
register_links(['form_view', 'about_view', 'license_view'], [form_view], menu_name='secondary_menu')

with transaction.commit_on_success():
    try:
        RegistrationSingleton.objects.get()
    except DatabaseError:
        transaction.rollback()
