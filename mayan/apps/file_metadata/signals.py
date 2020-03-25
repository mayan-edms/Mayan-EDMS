from django.dispatch import Signal

post_document_version_file_metadata_processing = Signal(
    providing_args=('instance',), use_caching=True
)
