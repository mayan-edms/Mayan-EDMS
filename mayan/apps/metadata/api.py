from django.shortcuts import get_object_or_404

from mayan.apps.views.http import URL

from .models import DocumentMetadata, MetadataType


def decode_metadata_from_querystring(querystring=None):
    """
    Parse a URL query string to a list of metadata
    """
    metadata_dict = {
        'id': {},
        'value': {}
    }
    metadata_list = []
    if querystring:
        # Match out of order metadata_type ids with metadata values from request
        for key, value in URL(query_string=querystring).args.items():
            if 'metadata' in key:
                index, element = key[8:].split('_')
                metadata_dict[element][index] = value

        # Convert the nested dictionary into a list of id+values dictionaries
        for order, identifier in metadata_dict['id'].items():
            if order in metadata_dict['value'].keys():
                metadata_list.append(
                    {
                        'id': identifier,
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
            klass=MetadataType, pk=metadata_dict['id']
        )
    }

    if create:
        # Use matched metadata now to create document metadata
        try:
            DocumentMetadata.objects.get(**parameters)
        except DocumentMetadata.DoesNotExist:
            document_metadata = DocumentMetadata(**parameters)
            document_metadata.save(_user=_user)
    else:
        try:
            document_metadata = DocumentMetadata.objects.get(
                document=document,
                metadata_type=get_object_or_404(
                    klass=MetadataType, pk=metadata_dict['id']
                ),
            )
        except DocumentMetadata.DoesNotExist:
            # TODO: Maybe return warning to caller?
            document_metadata = None

    if document_metadata:
        document_metadata.value = metadata_dict['value']
        document_metadata.save(_user=_user)


def metadata_repr(metadata_list):
    """
    Return a printable representation of a metadata list
    """
    return ', '.join(metadata_repr_as_list(metadata_list))


def metadata_repr_as_list(metadata_list):
    """
    Turn a list of metadata into a list of printable representations
    """
    output = []
    for metadata_dict in metadata_list:
        try:
            output.append('%s - %s' % (MetadataType.objects.get(
                pk=metadata_dict['id']), metadata_dict.get('value', '')))
        except Exception:
            pass

    return output


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
