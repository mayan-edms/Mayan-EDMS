import json
import logging

from furl import furl

from django.conf import settings
from django.core import mail
from django.db import models
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.literals import DOCUMENT_VERSION_EXPORT_MIMETYPE
from mayan.apps.storage.utils import TemporaryFile
from mayan.apps.templating.classes import Template

from .classes import NullBackend
from .events import event_email_sent
from .managers import UserMailerManager
from .utils import split_recipient_list

logger = logging.getLogger(name=__name__)


class UserMailer(models.Model):
    """
    This model is used to create mailing profiles that can be used from inside
    the system. These profiles differ from the system mailing profile in that
    they can be created at runtime and can be assigned ACLs to restrict
    their use.
    """
    label = models.CharField(
        help_text=_('A short text describing the mailing profile.'),
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
        verbose_name = _('Mailing profile')
        verbose_name_plural = _('Mailing profiles')

    def __str__(self):
        return self.label

    def backend_label(self):
        """
        Return the label that the backend itself provides. The backend is
        loaded but not initialized. As such the label returned is a class
        property.
        """
        return self.get_backend().label

    backend_label.short_description = _('Backend')
    backend_label.help_text = _('The backend class for this entry.')

    def dumps(self, data):
        """
        Serialize the backend configuration data.
        """
        self.backend_data = json.dumps(obj=data)
        self.save()

    def get_class_data(self):
        """
        Return the actual mailing class initialization data.
        """
        backend = self.get_backend()
        return {
            key: value for key, value in self.loads().items() if key in backend.get_class_fields()
        }

    def get_backend(self):
        """
        Retrieves the backend by importing the module and the class.
        """
        try:
            return import_string(dotted_path=self.backend_path)
        except ImportError:
            return NullBackend

    def get_connection(self):
        """
        Establishes a reusable connection to the server by loading the
        backend, initializing it, and the using the backend instance to get
        a connection.
        """
        return mail.get_connection(
            backend=self.get_backend().class_path, **self.get_class_data()
        )

    def loads(self):
        """
        Deserialize the stored backend data.
        """
        return json.loads(s=self.backend_data)

    def natural_key(self):
        return (self.label,)

    def save(self, *args, **kwargs):
        if self.default:
            UserMailer.objects.select_for_update().exclude(pk=self.pk).update(
                default=False
            )

        return super().save(*args, **kwargs)

    def send(
        self, to, attachments=None, subject='', body='', cc=None, bcc=None,
        reply_to=None, _event_action_object=None, _user=None
    ):
        """
        Send a simple email. There is no document or template knowledge.
        attachments is a list of dictionaries with the keys:
        filename, content, and  mimetype.
        """
        recipient_list = split_recipient_list(recipients=[to])

        if cc:
            cc_list = split_recipient_list(recipients=[cc])
        else:
            cc_list = None

        if bcc:
            bcc_list = split_recipient_list(recipients=[bcc])
        else:
            bcc_list = None

        if reply_to:
            reply_to_list = split_recipient_list(recipients=[reply_to])
        else:
            reply_to_list = None

        backend_data = self.loads()

        with self.get_connection() as connection:
            email_message = mail.EmailMultiAlternatives(
                body=strip_tags(body), connection=connection,
                from_email=backend_data.get('from'), subject=subject,
                to=recipient_list, cc=cc_list, bcc=bcc_list,
                reply_to=reply_to_list
            )

            for attachment in attachments or ():
                email_message.attach(
                    filename=attachment['filename'],
                    content=attachment['content'],
                    mimetype=attachment['mimetype']
                )

            email_message.attach_alternative(body, 'text/html')

        try:
            email_message.send()

        except Exception as exception:
            self.error_log.create(
                text='{}; {}'.format(
                    exception.__class__.__name__, exception
                )
            )
        else:
            self.error_log.all().delete()

            event_email_sent.commit(
                actor=_user, action_object=_event_action_object,
                target=self
            )

    def send_document(
        self, document, to, as_attachment=False, body='', cc=None, bcc=None,
        organization_installation_url='', reply_to=None, subject='',
        _user=None
    ):
        """
        Send a document using this user mailing profile.
        """
        context_dictionary = {
            'link': furl(organization_installation_url).join(
                document.get_absolute_url()
            ).tostr(),
            'document': document
        }

        body_template = Template(template_string=body)
        body_html_content = body_template.render(
            context=context_dictionary
        )

        subject_template = Template(template_string=subject)
        subject_text = strip_tags(
            subject_template.render(context=context_dictionary)
        )

        attachments = []
        if as_attachment:
            with TemporaryFile() as file_object:
                logger.debug('exporting document to send via email')
                document.version_active.export(file_object=file_object)
                file_object.seek(0)

                attachments.append(
                    {
                        'content': file_object.read(),
                        'filename': document.label,
                        'mimetype': DOCUMENT_VERSION_EXPORT_MIMETYPE
                    }
                )

        return self.send(
            attachments=attachments, cc=cc, bcc=bcc, body=body_html_content,
            reply_to=reply_to, subject=subject_text, to=to,
            _event_action_object=document, _user=_user
        )

    def test(self, to):
        """
        Send a test message to make sure the mailing profile settings are
        correct.
        """
        try:
            self.send(subject=_('Test email from Mayan EDMS'), to=to)
        except Exception as exception:
            self.error_log.create(
                text='{}; {}'.format(
                    exception.__class__.__name__, exception
                )
            )
            if settings.DEBUG:
                raise
        else:
            self.error_log.all().delete()
