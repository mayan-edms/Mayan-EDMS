from __future__ import unicode_literals

import json
import logging

from django.contrib.sites.models import Site
from django.core import mail
from django.db import models
from django.template import Context, Template
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from .managers import UserMailerManager
from .utils import split_recipient_list

logger = logging.getLogger(__name__)


class LogEntry(models.Model):
    datetime = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_('Date time')
    )
    message = models.TextField(
        blank=True, editable=False, verbose_name=_('Message')
    )

    class Meta:
        get_latest_by = 'datetime'
        ordering = ('-datetime',)
        verbose_name = _('Log entry')
        verbose_name_plural = _('Log entries')


class UserMailer(models.Model):
    label = models.CharField(
        max_length=128, unique=True, verbose_name=_('Label')
    )
    default = models.BooleanField(
        default=True, help_text=_(
            'If default, this mailing profile will be pre-selected on the '
            'document mailing form.'
        ), verbose_name=_('Default')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    backend_path = models.CharField(
        max_length=128,
        help_text=_('The dotted Python path to the backend class.'),
        verbose_name=_('Backend path')
    )
    backend_data = models.TextField(
        blank=True, verbose_name=_('Backend data')
    )

    objects = UserMailerManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('User mailer')
        verbose_name_plural = _('User mailers')

    def __str__(self):
        return self.label

    def backend_label(self):
        return self.get_backend().label

    def dumps(self, data):
        self.backend_data = json.dumps(data)
        self.save()

    def get_backend(self):
        return import_string(self.backend_path)

    def get_connection(self):
        return mail.get_connection(
            backend=self.get_backend().class_path, **self.loads()
        )

    def loads(self):
        return json.loads(self.backend_data)

    def natural_key(self):
        return (self.label,)

    def save(self, *args, **kwargs):
        if self.default:
            UserMailer.objects.select_for_update().exclude(pk=self.pk).update(
                default=False
            )

        return super(UserMailer, self).save(*args, **kwargs)

    def send(self, to, subject='', body='', attachments=None):
        """
        Send a simple email. There is no document or template knowledge.
        attachments is a list of dictionaries with the keys:
        filename, content, and  mimetype.
        """
        recipient_list = split_recipient_list(recipients=[to])

        with self.get_connection() as connection:
            email_message = mail.EmailMultiAlternatives(
                body=strip_tags(body), connection=connection, subject=subject,
                to=recipient_list,
            )

            for attachment in attachments or []:
                email_message.attach(
                    filename=attachment['filename'],
                    content=attachment['content'],
                    mimetype=attachment['mimetype']
                )

            email_message.attach_alternative(body, 'text/html')

            try:
                email_message.send()
            except Exception as exception:
                self.error_log.create(message=exception)
            else:
                self.error_log.all().delete()

    def send_document(self, document, to, subject='', body='', as_attachment=False):
        context_dictionary = {
            'link': 'http://%s%s' % (
                Site.objects.get_current().domain,
                document.get_absolute_url()
            ),
            'document': document
        }

        context = Context(context_dictionary)

        body_template = Template(body)
        body_html_content = body_template.render(context)

        subject_template = Template(subject)
        subject_text = strip_tags(subject_template.render(context))

        attachments = []
        if as_attachment:
            with document.open() as file_object:
                attachments.append(
                    {
                        'filename': document.label, 'content': file_object.read(),
                        'mimetype': document.file_mimetype
                    }
                )

        return self.send(
            subject=subject_text, body=body_html_content, to=to, attachments=attachments
        )

    def test(self, to):
        self.send(subject=_('Test email from Mayan EDMS'), to=to)


class UserMailerLogEntry(models.Model):
    user_mailer = models.ForeignKey(
        on_delete=models.CASCADE, related_name='error_log', to=UserMailer,
        verbose_name=_('User mailer')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_('Date time')
    )
    message = models.TextField(
        blank=True, editable=False, verbose_name=_('Message')
    )

    class Meta:
        get_latest_by = 'datetime'
        ordering = ('-datetime',)
        verbose_name = _('User mailer log entry')
        verbose_name_plural = _('User mailer log entries')
