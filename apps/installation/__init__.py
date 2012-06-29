from __future__ import absolute_import

from south.signals import post_migrate

from project_tools.api import register_tool

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.utils import DatabaseError

from .links import installation_details
from .models import Installation
    

@receiver(post_migrate, dispatch_uid='trigger_first_time')
def trigger_first_time(sender, **kwargs):
    if kwargs['app'] == 'installation':
        details = Installation.objects.get()
        details.is_first_run = True
        details.save()


def check_first_run():
    try:
        details = Installation.objects.get()
    except DatabaseError:
        # Avoid database errors when the app tables haven't been created yet
        pass
    else:
        if details.is_first_run:
            details.submit()


register_tool(installation_details)

check_first_run()
