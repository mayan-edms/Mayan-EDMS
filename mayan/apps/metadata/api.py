from django.shortcuts import get_object_or_404

from mayan.apps.views.http import URL

from .models import DocumentMetadata, MetadataType


def decode_metadata_from_querystring(querystring=None):
    """
    Parse a URL query string to a list of metadata
    """
    metadata_dict = {
        'metadata_type_id': {},
        'value': {}
    }
    metadata_list = []
    if querystring:
        # Match out of order metadata_type ids with metadata values from request
        for key, value in URL(query_string=querystring).args.items():
            if key.startswith('metadata'):
                index, element = key.split('_', 1)
                index = index[8:]
                metadata_dict[element][index] = value

        # Convert the nested dictionary into a list of id+values dictionaries
        for order, identifier in metadata_dict['metadata_type_id'].items():
            if order in metadata_dict['value'].keys():
                metadata_list.append(
                    {
                        'metadata_type_id': identifier,
                        'value': metadata_dict['value'][order]
                    }
                )

    return metadata_list


def save_metadata_list(metadata_list, document, create=False, _user=None):
    """
    Take a list of metadata dictionaries and associate them to a
    document
    """
    for item in metadata_list:
        save_metadata(
            metadata_dict=item, document=document, create=create, _user=_user
        )


def save_metadata(metadata_dict, document, create=False, _user=None):
    """
    Take a dictionary of metadata type & value and associate it to a
    document
    """
    parameters = {
        'document': document,
        'metadata_type': get_object_or_404(
            klass=MetadataType, pk=metadata_dict['metadata_type_id']
        )
    }

    if create:
        # Use matched metadata now to create document metadata.
        try:
            DocumentMetadata.objects.get(**parameters)
        except DocumentMetadata.DoesNotExist:
            document_metadata = DocumentMetadata(**parameters)
            document_metadata._event_actior = _user
            document_metadata.save()
    else:
        try:
            document_metadata = DocumentMetadata.objects.get(
                document=document,
                metadata_type=get_object_or_404(
                    klass=MetadataType, pk=metadata_dict['metadata_type_id']
                ),
            )
        except DocumentMetadata.DoesNotExist:
            document_metadata = None

    if document_metadata:
        document_metadata.value = metadata_dict['value']
        document_metadata._event_actor = _user
        document_metadata.save()


def set_bulk_metadata(document, metadata_dictionary):
    document_type_metadata_types = document.document_type.metadata.values_list(
        'metadata_type', flat=True
    )

    for metadata_type_name, value in metadata_dictionary.items():
        metadata_type = MetadataType.objects.get(name=metadata_type_name)

        if document_type_metadata_types.filter(metadata_type=metadata_type).exists():
            DocumentMetadata.objects.get_or_create(
                document=document, metadata_type=metadata_type, value=value
            )
