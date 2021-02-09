from django.dispatch import Signal

signal_post_document_file_parsing = Signal(
    providing_args=('instance',), use_caching=True
)
