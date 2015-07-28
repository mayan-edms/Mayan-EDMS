from __future__ import unicode_literals

from kombu import Exchange, Queue

from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import MayanAppConfig, menu_object
from documents.models import Document
from mayan.celery import app

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

        app.conf.CELERY_QUEUES.append(
            Queue('mailing', Exchange('mailing'), routing_key='mailing'),
        )

        app.conf.CELERY_ROUTES.update(
            {
                'mailer.tasks.task_send_document': {
                    'queue': 'mailing'
                },
            }
        )

        menu_object.bind_links(
            links=(
                link_send_document_link, link_send_document
            ), sources=(Document,)
        )
