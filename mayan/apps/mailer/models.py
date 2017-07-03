from __future__ import unicode_literals

import json
import logging

from django.core import mail
from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

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
        max_length=32, unique=True, verbose_name=_('Label')
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

    class Meta:
        ordering = ('label',)
        verbose_name = _('User mailer')
        verbose_name_plural = _('User mailers')

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if self.default:
            UserMailer.objects.select_for_update().exclude(pk=self.pk).update(
                default=False
            )

        return super(UserMailer, self).save(*args, **kwargs)

    def backend_label(self):
        return self.get_backend().label

    def get_backend(self):
        return import_string(self.backend_path)

    def get_connection(self):
        return mail.get_connection(
            backend=self.get_backend().class_path, **self.loads()
        )

    def loads(self):
        return json.loads(self.backend_data)

    def dumps(self, data):
        self.backend_data = json.dumps(data)
        self.save()

    def send(self, **kwargs):
        """
        https://docs.djangoproject.com/en/1.11/topics/email
        #django.core.mail.EmailMessage
        subject: The subject line of the email.
        body: The body text. This should be a plain text message.
        from_email: The sender's address. Both fred@example.com and Fred
        <fred@example.com> forms are legal. If omitted,
        the DEFAULT_FROM_EMAIL setting is used.
        to: A list or tuple of recipient addresses.
        bcc: A list or tuple of addresses used in the "Bcc" header when
        sending the email.
        connection: An email backend instance. Use this parameter if you want
        to use the same connection for multiple messages. If omitted, a new
        connection is created when send() is called.
        attachments: A list of attachments to put on the message. These can be
        either email.MIMEBase.MIMEBase instances, or (filename, content,
        mimetype) triples.
        headers: A dictionary of extra headers to put on the message. The
        keys are the header name, values are the header values. It's up to
        the caller to ensure header names and values are in the correct
        format for an email message. The corresponding attribute is
        extra_headers.
        cc: A list or tuple of recipient addresses used in the "Cc"
        header when sending the email.
        reply_to: A list or tuple of recipient addresses used in the
        "Reply-To" header when sending the email.
        """
        with self.get_connection() as connection:
            mail.EmailMessage(connection=connection, **kwargs).send()

    def test(self, to):
        self.send(to=to, subject=_('Test email from Mayan EDMS'))


class UserMailerLogEntry(models.Model):
    user_mailer = models.ForeignKey(
        UserMailer, related_name='error_log', verbose_name=_('User mailer')
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
