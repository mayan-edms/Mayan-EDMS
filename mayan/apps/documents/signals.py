from django.dispatch import Signal

signal_post_document_created = Signal(
    providing_args=('instance',), use_caching=True
)
signal_post_document_type_change = Signal(
    providing_args=('instance',), use_caching=True
)
signal_post_initial_document_type = Signal(
    providing_args=('instance',), use_caching=True
)
signal_post_document_file_upload = Signal(
    providing_args=('instance',), use_caching=True
)
signal_post_document_version_remap = Signal(
    providing_args=('instance',), use_caching=True
)
