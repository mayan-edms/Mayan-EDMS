from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import MayanAppConfig, menu_object
from documents.models import Document

from .links import link_send_document_link, link_send_document
from .permissions import (
    permission_mailing_link, permission_mailing_send_document
)


class MailerApp(MayanAppConfig):
    name = 'mailer'
    verbose_name = _('Mailer')

    def ready(self):
        super(MailerApp, self).ready()

        ModelPermission.register(
            model=Document, permissions=(
                permission_mailing_link, permission_mailing_send_document
            )
        )

        menu_object.bind_links(links=[link_send_document_link, link_send_document], sources=[Document])
