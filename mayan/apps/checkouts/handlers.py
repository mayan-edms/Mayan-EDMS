from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .exceptions import NewDocumentVersionNotAllowed
from .models import DocumentCheckout


def check_if_new_versions_allowed(sender, **kwargs):
    if not DocumentCheckout.objects.are_document_new_versions_allowed(kwargs['instance'].document):
        raise NewDocumentVersionNotAllowed(
            _(
                'New versions not allowed for the checkedout document: %s'
                % kwargs['instance'].document
            )
        )
