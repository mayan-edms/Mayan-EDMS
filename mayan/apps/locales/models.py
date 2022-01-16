from pytz import common_timezones

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import event_user_locale_profile_edited
from .managers import UserLocaleProfileManager


class UserLocaleProfile(models.Model):
    """
    Stores the locale preferences of a user. Stores timezone and language
    at the moment.
    """
    user = models.OneToOneField(
        on_delete=models.CASCADE, related_name='locale_profile',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    timezone = models.CharField(
        choices=zip(common_timezones, common_timezones), max_length=48,
        verbose_name=_('Timezone')
    )
    language = models.CharField(
        choices=settings.LANGUAGES, max_length=8, verbose_name=_('Language')
    )

    objects = UserLocaleProfileManager()

    class Meta:
        verbose_name = _('User locale profile')
        verbose_name_plural = _('User locale profiles')

    def __str__(self):
        return '{} ({}, {})'.format(
            self.user, self.language or _('None'), self.timezone or _('None')
        )

    def natural_key(self):
        return self.user.natural_key()
    natural_key.dependencies = [settings.AUTH_USER_MODEL]

    @method_event(
        event_manager_class=EventManagerSave,
        edited={
            'event': event_user_locale_profile_edited,
            'target': 'user'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
