from django.dispatch import Signal

signal_post_document_file_file_metadata_processing = Signal(
    providing_args=('instance',), use_caching=True
)
