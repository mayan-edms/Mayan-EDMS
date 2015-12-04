from __future__ import unicode_literals

from django.dispatch import Signal

post_version_upload = Signal(providing_args=('instance',), use_caching=True)
post_document_type_change = Signal(
    providing_args=('instance',), use_caching=True
)
post_document_created = Signal(providing_args=('instance',), use_caching=True)
