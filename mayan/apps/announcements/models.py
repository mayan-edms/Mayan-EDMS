from django.db import models
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import event_announcement_created, event_announcement_edited
from .managers import AnnouncementManager


class Announcement(ExtraDataModelMixin, models.Model):
    """
    Model to store an information announcement that will be displayed at the
    login screen. Announcements can have an activation and deactivation date.
    """
    label = models.CharField(
        max_length=32, help_text=_('Short description of this announcement.'),
        verbose_name=_('Label')
    )
    text = models.TextField(
        help_text=_('The actual text to be displayed.'),
        verbose_name=_('Text')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    start_datetime = models.DateTimeField(
        blank=True, help_text=_(
            'Date and time after which this announcement will be displayed.'
        ), null=True, verbose_name=_('Start date time')
    )
    end_datetime = models.DateTimeField(
        blank=True, help_text=_(
            'Date and time until when this announcement is to be displayed.'
        ), null=True, verbose_name=_('End date time')
    )

    objects = AnnouncementManager()

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')

    def __str__(self):
        return self.label

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_announcement_created,
            'target': 'self',
        },
        edited={
            'event': event_announcement_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
