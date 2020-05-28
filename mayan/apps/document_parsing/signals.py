from django.dispatch import Signal

signal_post_document_version_parsing = Signal(
    providing_args=('instance',), use_caching=True
)
