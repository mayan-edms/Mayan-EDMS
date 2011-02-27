import os
import tempfile
from urllib import unquote_plus

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from documents import TEMPORARY_DIRECTORY

from models import Document, DocumentMetadata, MetadataType

#http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(source, dest, buffer_size=1024*1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    if not hasattr(source, 'read'):
        source = open(source, 'rb')
    if not hasattr(dest, 'write'):
        dest = open(dest, 'wb')

    while 1:
        copy_buffer = source.read(buffer_size)
        if copy_buffer:
            dest.write(copy_buffer)
        else:
            break

    source.close()
    dest.close()


def from_descriptor_to_tempfile(input_descriptor, filename, buffer_size=1024*1024):
    path = os.path.join(TEMPORARY_DIRECTORY, filename)
    
    output_descriptor = open(path, 'wb')
    
    while 1:
        copy_buffer = input_descriptor.read(buffer_size)
        if copy_buffer:
            output_descriptor.write(copy_buffer)
        else:
            break

    input_descriptor.close()
    output_descriptor.close()
    return path


def from_descriptor_to_new_tempfile(input_descriptor, buffer_size=1024*1024):
    output_descriptor, tmp_filename = tempfile.mkstemp()
    
    while 1:
        copy_buffer = input_descriptor.read(buffer_size)
        if copy_buffer:
            #output_descriptor.write(copy_buffer)
            os.write(output_descriptor, copy_buffer)
        else:
            break

    input_descriptor.close()
    os.close(output_descriptor)
    return tmp_filename


def decode_metadata_from_url(url_dict):
    metadata_dict = {
        'id':{},
        'value':{}
    }
    metadata_list = []
    #Match out of order metadata_type ids with metadata values from request
    for key, value in url_dict.items():
        if 'metadata' in key:
            index, element = key[8:].split('_')
            metadata_dict[element][index] = value
        
    #Convert the nested dictionary into a list of id+values dictionaries
    for order, id in metadata_dict['id'].items():
        if order in metadata_dict['value'].keys():
            metadata_list.append({'id':id, 'value':metadata_dict['value'][order]})

    return metadata_list
    
    
def save_metadata_list(metadata_list, document):
    for item in metadata_list:
        if item['value']:
            save_metadata(item, document)
        else:
            try:
                metadata_type = MetadataType.objects.get(id=item['id'])
                document_metadata = DocumentMetadata.objects.get(document=document,
                    metadata_type=metadata_type)
                document_metadata.delete()
            except ObjectDoesNotExist:
                pass
                        
        
def save_metadata(metadata_dict, document):
    #Use matched metadata now to create document metadata
    document_metadata, created = DocumentMetadata.objects.get_or_create(
        document=document,
        metadata_type=get_object_or_404(MetadataType, pk=metadata_dict['id']),
    )
    #Handle 'plus sign as space' in the url
    
    #unquote_plus handles utf-8?!?
    #http://stackoverflow.com/questions/4382875/handling-iri-in-django
    document_metadata.value=unquote_plus(metadata_dict['value'])#.decode('utf-8')
    document_metadata.save()
