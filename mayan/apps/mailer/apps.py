from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common import menu_object
from documents.models import Document

from .links import link_send_document_link, link_send_document
from .permissions import (
    PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
)


class MailerApp(apps.AppConfig):
    name = 'mailer'
    verbose_name = _('Mailer')

    def ready(self):
        menu_object.bind_links(links=[link_send_document_link, link_send_document], sources=[Document])

        class_permissions(Document, [
            PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
        ])
