from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bleach import Cleaner
from bleach.linkifier import LinkifyFilter

from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event
from mayan.apps.templating.classes import Template

from .events import event_message_created, event_message_edited


class Message(models.Model):
    sender_content_type = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE, to=ContentType
    )
    sender_object_id = models.PositiveIntegerField(blank=True, null=True)
    sender_object = GenericForeignKey(
        ct_field='sender_content_type', fk_field='sender_object_id'
    )
    user = models.ForeignKey(
        db_index=True, on_delete=models.CASCADE,
        related_name='messages', to=settings.AUTH_USER_MODEL,
        verbose_name=_('User')
    )
    subject = models.CharField(
        max_length=255, help_text=_('Short description of this message.'),
        verbose_name=_('Subject')
    )
    body = models.TextField(
        help_text=_('The actual content of the message.'),
        verbose_name=_('Body')
    )
    read = models.BooleanField(
        default=False, help_text=_(
            'This field determines if the message has been read or not.'
        ), verbose_name=_('Read')
    )
    date_time = models.DateTimeField(
        auto_now_add=True, help_text=_(
            'Date and time of the message creation.'
        ), verbose_name=_('Creation date and time')
    )

    class Meta:
        ordering = ('-date_time',)
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.get_label()

    def get_absolute_url(self):
        return reverse(
            viewname='messaging:message_detail', kwargs={'message_id': self.pk}
        )

    def get_label(self):
        return Template(
            template_string='{{ instance.date_time }} @{{ instance.sender_object }} "{{ instance.subject }}"'
        ).render(
            context={'instance': self}
        )
    get_label.short_description = _('Label')

    def get_rendered_body(self):
        cleaner = Cleaner(
            filters=[LinkifyFilter]
        )

        template = Template(
            template_string=cleaner.clean(text=self.body)
        )
        return template.render(context={'message': self})

    def mark_read(self):
        self.read = True
        self.save(update_fields=('read',))

    def mark_unread(self):
        self.read = False
        self.save(update_fields=('read',))

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
