from __future__ import unicode_literals


def get_metadata_string(document):
    """
    Return a formated representation of a document's metadata values
    """
    return ', '.join(
        [
            '%s - %s' % (
                document_metadata.metadata_type, document_metadata.value
            ) for document_metadata in document.metadata.all()
        ]
    )
