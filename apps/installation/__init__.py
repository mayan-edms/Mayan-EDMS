from __future__ import absolute_import

from south.signals import post_migrate

from django.dispatch import receiver
from django.db.utils import DatabaseError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

#from backups.api import AppBackup, ModelBackup
#from app_registry import register_app, UnableToRegister
from project_tools.api import register_tool

from .links import installation_details
from .models import Installation


@receiver(post_migrate, dispatch_uid='trigger_first_time')
def trigger_first_time(sender, **kwargs):
    if kwargs['app'] == 'installation':
        details = Installation.objects.get()
        details.is_first_run = True
        details.save()


@transaction.commit_on_success
def check_first_run():
    try:
        details = Installation.get()
    except DatabaseError:
        # Avoid database errors when the app tables haven't been created yet
        transaction.rollback()
    else:
        if details.is_first_run:
            details.submit()


register_tool(installation_details)

check_first_run()
