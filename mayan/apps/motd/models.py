from django.db import models
from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import event_message_created, event_message_edited
from .managers import MessageManager


class Message(models.Model):
    """
    Model to store an information message that will be displayed at the login
    screen. Messages can have an activation and deactivation date.
    """
    label = models.CharField(
        max_length=32, help_text=_('Short description of this message.'),
        verbose_name=_('Label')
    )
    message = models.TextField(
        help_text=_('The actual message to be displayed.'),
        verbose_name=_('Message')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    start_datetime = models.DateTimeField(
        blank=True, help_text=_(
            'Date and time after which this message will be displayed.'
        ), null=True, verbose_name=_('Start date time')
    )
    end_datetime = models.DateTimeField(
        blank=True, help_text=_(
            'Date and time until when this message is to be displayed.'
        ), null=True, verbose_name=_('End date time')
    )

    objects = MessageManager()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.label

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_message_created,
            'target': 'self',
        },
        edited={
            'event': event_message_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
