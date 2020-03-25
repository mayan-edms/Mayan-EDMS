from django.dispatch import Signal

post_document_version_ocr = Signal(
    providing_args=('instance',), use_caching=True
)
