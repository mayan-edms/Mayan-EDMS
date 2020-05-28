from django.dispatch import Signal

signal_post_document_version_ocr = Signal(
    providing_args=('instance',), use_caching=True
)
