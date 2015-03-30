from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from documents.models import Document
from navigation.api import register_links

from .links import send_document_link, send_document
from .permissions import (
    PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
)


class MailerApp(apps.AppConfig):
    name = 'mailer'
    verbose_name = _('Mailer')

    def ready(self):
        register_links([Document], [send_document_link, send_document])

        class_permissions(Document, [
            PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
        ])
