from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import MayanAppConfig, menu_facet, menu_main, menu_sidebar
from documents.models import Document, DocumentVersion
from mayan.celery import app
from rest_api.classes import APIEndPoint

from .handlers import check_if_new_versions_allowed
from .links import (
    link_checkin_document, link_checkout_document, link_checkout_info,
    link_checkout_list
)
from .models import DocumentCheckout
from .permissions import (
    permission_document_checkin, permission_document_checkin_override,
    permission_document_checkout
)

CHECK_EXPIRED_CHECK_OUTS_INTERVAL = 60  # Lowest check out expiration allowed


class CheckoutsApp(MayanAppConfig):
    name = 'checkouts'
    verbose_name = _('Checkouts')

    def ready(self):
        super(CheckoutsApp, self).ready()

        APIEndPoint('checkouts')

        Document.add_to_class('is_checked_out', lambda document: DocumentCheckout.objects.is_document_checked_out(document))
        Document.add_to_class('check_in', lambda document, user=None: DocumentCheckout.objects.check_in_document(document, user))
        Document.add_to_class('checkout_info', lambda document: DocumentCheckout.objects.document_checkout_info(document))
        Document.add_to_class('checkout_state', lambda document: DocumentCheckout.objects.document_checkout_state(document))

        app.conf.CELERYBEAT_SCHEDULE.update({
            'check_expired_check_outs': {
                'task': 'checkouts.tasks.task_check_expired_check_outs',
                'schedule': timedelta(seconds=CHECK_EXPIRED_CHECK_OUTS_INTERVAL),
                'options': {'queue': 'checkouts'}
            },
        })

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_checkout,
                permission_document_checkin,
                permission_document_checkin_override,
            )
        )

        menu_facet.bind_links(links=[link_checkout_info], sources=[Document])
        menu_main.bind_links(links=[link_checkout_list])
        menu_sidebar.bind_links(links=[link_checkout_document, link_checkin_document], sources=['checkouts:checkout_info', 'checkouts:checkout_document', 'checkouts:checkin_document'])

        pre_save.connect(check_if_new_versions_allowed, dispatch_uid='document_index_delete', sender=DocumentVersion)
