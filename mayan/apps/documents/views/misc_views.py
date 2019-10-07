from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import ConfirmView

from ..permissions import permission_document_tools
from ..tasks import task_scan_duplicates_all

__all__ = ('ScanDuplicatedDocuments',)
logger = logging.getLogger(__name__)


class ScanDuplicatedDocuments(ConfirmView):
    extra_context = {
        'title': _('Scan for duplicated documents?')
    }
    view_permission = permission_document_tools

    def view_action(self):
        task_scan_duplicates_all.apply_async()
        messages.success(
            message=_('Duplicated document scan queued successfully.'),
            request=self.request
        )
