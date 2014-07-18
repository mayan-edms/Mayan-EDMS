from __future__ import absolute_import

from django.dispatch import receiver

from south.signals import post_migrate

from common import about_view, license_view
from navigation.api import register_links

from .links import form_view
from .models import RegistrationSingleton

register_links(['form_view'], [about_view, license_view], menu_name='secondary_menu')
register_links(['form_view', 'about_view', 'license_view'], [form_view], menu_name='secondary_menu')


@receiver(post_migrate, dispatch_uid='trigger_first_time', sender=RegistrationSingleton)
def trigger_first_time(sender, **kwargs):
    RegistrationSingleton.objects.get_or_create()
