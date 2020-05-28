from django.dispatch import Signal

signal_post_document_version_file_metadata_processing = Signal(
    providing_args=('instance',), use_caching=True
)
