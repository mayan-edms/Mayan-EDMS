"""
Metadata handling commonalities
"""

from __future__ import absolute_import

from urllib import unquote_plus

from django.shortcuts import get_object_or_404

from .models import DocumentMetadata, MetadataType


def decode_metadata_from_url(url_dict):
    """
    Parse a URL query string to a list of metadata
    """
    metadata_dict = {
        'id': {},
        'value': {}
    }
    metadata_list = []
    #Match out of order metadata_type ids with metadata values from request
    for key, value in url_dict.items():
        if 'metadata' in key:
            index, element = key[8:].split('_')
            metadata_dict[element][index] = value

    #Convert the nested dictionary into a list of id+values dictionaries
    for order, identifier in metadata_dict['id'].items():
        if order in metadata_dict['value'].keys():
            metadata_list.append({
                'id': identifier,
                'value': metadata_dict['value'][order]
            })

    return metadata_list


def save_metadata_list(metadata_list, document, create=False):
    """
    Take a list of metadata dictionaries and associate them to a
    document
    """
    for item in metadata_list:
        save_metadata(item, document, create)


def save_metadata(metadata_dict, document, create=False):
    """
    Take a dictionary of metadata type & value and associate it to a
    document
    """
    if create:
        # Use matched metadata now to create document metadata
        document_metadata, created = DocumentMetadata.objects.get_or_create(
            document=document,
            metadata_type=get_object_or_404(
                MetadataType,
                pk=metadata_dict['id']
           ),
        )
    else:
        try:
            document_metadata = DocumentMetadata.objects.get(
                document=document,
                metadata_type=get_object_or_404(
                    MetadataType,
                    pk=metadata_dict['id']
                ),
            )
        except DocumentMetadata.DoesNotExist:
            # TODO: Maybe return warning to caller?
            document_metadata = None

    # Handle 'plus sign as space' in the url

    # unquote_plus handles utf-8?!?
    # http://stackoverflow.com/questions/4382875/handling-iri-in-django
    #.decode('utf-8')
    if document_metadata:
        document_metadata.value = unquote_plus(metadata_dict['value'])
        document_metadata.save()


def metadata_repr(metadata_list):
    """
    Return a printable representation of a metadata list
    """
    return u', '.join(metadata_repr_as_list(metadata_list))


def metadata_repr_as_list(metadata_list):
    """
    Turn a list of metadata into a list of printable representations
    """
    output = []
    for metadata_dict in metadata_list:
        try:
            output.append(u'%s - %s' % (MetadataType.objects.get(
                pk=metadata_dict['id']), metadata_dict.get('value', '')))
        except:
            pass

    return output


def get_metadata_string(document):
    """
    Return a formated representation of a document's metadata values
    """
    return u', '.join([u'%s - %s' % (metadata.metadata_type, metadata.value) for metadata in DocumentMetadata.objects.filter(document=document).select_related('metadata_type')])


def convert_dict_to_dict_list(dictionary):
    result = []
    for key, value in dictionary.items():
        try:
            metadata_type = MetadataType.objects.get(name=key)
        except MetadataType.DoesNotExist:
            raise ValueError('Unknown metadata type name')
        result.append({'id': metadata_type.pk, 'value': value})

    return result
