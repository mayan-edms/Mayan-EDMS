from __future__ import unicode_literals

from django.dispatch import Signal

post_document_version_parsing = Signal(
    providing_args=('instance',), use_caching=True
)
