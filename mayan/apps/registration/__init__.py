from django.dispatch import receiver

from south.signals import post_migrate

from navigation.api import register_links

from .links import form_view
from .models import RegistrationSingleton

register_links(['registration:form_view', 'common:about_view', 'common:license_view'], [form_view], menu_name='secondary_menu')


@receiver(post_migrate, dispatch_uid='create_registration_instance')
def create_registration_instance(sender, **kwargs):
    if kwargs['app'] == 'registration':
        RegistrationSingleton.objects.get_or_create()
